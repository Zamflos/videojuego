# objects.py
import pygame
import os
import re
import random
import math
from constants import *

class WorldObject:
    def __init__(self, obj_type, pos, scale=1.0):
        self.type = obj_type
        self.pos = list(pos)
        self.scale = scale
        self.size = int(PIXEL_SCALE * scale)
        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)
        if obj_type == 'health_pack':
            self.state = 'idle'
            self.current_anim = 'idle'
        else:
            self.state = 'closed' if obj_type == 'crate' else 'off' if obj_type == 'campfire' else 'idle'
            self.current_anim = 'closed' if obj_type == 'crate' else 'off' if obj_type == 'campfire' else 'idle'
        self.frame_idx = 0
        self.anim_timer = 0.0
        self.frame_duration = 0.15
        self.active = True
        self.timer = 0.0
        self.animations = {}
        self.load_animations()

    def load_animations(self):
        base_path = os.path.join('Sprites', 'objects', self.type)
        print(f"[DEBUG] Buscando sprites en: {base_path}")  # ← ESTO TE DICE SI ENCUENTRA LA CARPETA
        
        if not os.path.exists(base_path):
            print(f"[ERROR] No existe la carpeta: {base_path}")
            return

        anim_map = {
            'crate': ['closed', 'open'],
            'campfire': ['off', 'on'],
            'wall': ['idle'],
            'health_pack': ['idle']  # Nueva animación para botiquín
        }
        
        for anim_name in anim_map.get(self.type, []):
            path = os.path.join(base_path, anim_name)
            if not os.path.exists(path):
                print(f"[ERROR] Falta carpeta: {path}")
                continue
                
            files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not files:
                print(f"[ERROR] No hay imágenes en: {path}")
                continue
                
            files.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
            frames = []
            for f in files:
                img_path = os.path.join(path, f)
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    scaled = pygame.transform.scale(img, (self.size, self.size))
                    frames.append(scaled)
                    print(f"[OK] Cargado: {img_path}")
                except Exception as e:
                    print(f"[ERROR] Falló al cargar {img_path}: {e}")
            
            if frames:
                self.animations[anim_name] = frames
                print(f"[OK] Animación '{anim_name}' cargada con {len(frames)} frames")
            else:
                self.animations[anim_name] = None

    def update(self, dt, player_pos):
        self.rect.topleft = self.pos
        if self.type == 'crate' and self.state == 'open' and self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.state = 'closed'
                self.current_anim = 'closed'

        anim = self.animations.get(self.current_anim, [])
        if anim and len(anim) > 1:
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer = 0
                self.frame_idx = (self.frame_idx + 1) % len(anim)

    def interact(self, player_pos):
        if not self.active: return None
        dist = math.hypot(player_pos[0] - (self.pos[0] + self.size//2), 
                         player_pos[1] - (self.pos[1] + self.size//2))
        if dist > 50: return None

        if self.type == 'crate' and self.state == 'closed':
            self.state = 'open'
            self.current_anim = 'open'
            self.timer = 30.0
            weights = [35, 25, CRATE_HINT_CHANCE, 10]  # ← 30% hints
            return random.choices(['energy', 'health', 'hint', 'fragment'], weights=weights)[0]
            
        elif self.type == 'campfire' and self.state == 'off':
            self.state = 'on'
            self.current_anim = 'on'
            return 'light_boost'
        
        elif self.type == 'health_pack':  # Nueva interacción para botiquín
            self.active = False
            return 'health'
            
        return None

    def draw(self, screen):
        if not self.active: return
        anim = self.animations.get(self.current_anim, [])
        if anim:
            frame = anim[self.frame_idx]
            screen.blit(frame, self.pos)
        else:
            # Fallback visual si no carga sprite
            if self.type == 'health_pack':  # Fallback para botiquín: rect verde con cruz roja
                color = (0, 255, 0)  # Verde para botiquín
                pygame.draw.rect(screen, color, (*self.pos, self.size, self.size))
                # Dibujar una cruz roja simple
                cross_color = (255, 0, 0)
                center_x = self.pos[0] + self.size // 2
                center_y = self.pos[1] + self.size // 2
                half = self.size // 4
                pygame.draw.rect(screen, cross_color, (center_x - half, center_y - 2, half * 2, 4))  # Horizontal
                pygame.draw.rect(screen, cross_color, (center_x - 2, center_y - half, 4, half * 2))  # Vertical
            else:
                color = (150, 100, 50) if self.type == 'crate' else (100, 100, 100) if self.type == 'wall' else (80, 40, 20)
                pygame.draw.rect(screen, color, (*self.pos, self.size, self.size))
            font = pygame.font.SysFont(None, 20)
            text = font.render(self.type.upper(), True, (255,255,255))
            screen.blit(text, (self.pos[0]+2, self.pos[1]+2))