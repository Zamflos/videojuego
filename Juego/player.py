# player.py → VERSIÓN FINAL 100% FUNCIONAL (con update corregido)
import pygame
import os
import re
import math
from constants import *

class Player:
    def __init__(self):
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.max_shadow_energy = MAX_SHADOW_ENERGY
        self.shadow_energy = MAX_SHADOW_ENERGY
        self.energy_regen_rate = ENERGY_REGEN_RATE
        self.health = 100
        self.obstacles = []
        self.hidden = False
        
        # Animaciones
        self.facing = 'front'
        self.current_anim = 'idle_front'
        self.frame_idx = 0
        self.anim_timer = 0.0
        self.frame_duration = 0.12
        self.rect = pygame.Rect(0, 0, PIXEL_SCALE, PIXEL_SCALE)
        self.animations = {}
        
        self.load_animations()

    def load_animations(self):
        sprite_folder = 'sprites/player'
        anim_folders = [
            'idle_front', 'idle_back', 'idle_left', 'idle_right',
            'walk_front', 'walk_back', 'walk_left', 'walk_right'
        ]
        
        def natural_sort_key(s):
            def convert(c):
                return int(c) if c.isdigit() else c.lower()
            return [convert(c) for c in re.split(r'([0-9]+)', s)]
        
        for folder in anim_folders:
            path = os.path.join(sprite_folder, folder)
            if not os.path.exists(path):
                print(f"ADVERTENCIA: Carpeta '{path}' no encontrada.")
                self.animations[folder] = None
                continue
            
            files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not files:
                self.animations[folder] = None
                continue
            
            files.sort(key=natural_sort_key)
            frames = []
            for f in files:
                img_path = os.path.join(path, f)
                try:
                    img = pygame.image.load(img_path)
                    scaled = pygame.transform.scale(img, (PIXEL_SCALE, PIXEL_SCALE))
                    frames.append(scaled)
                except Exception as e:
                    print(f"Error cargando {img_path}: {e}")
            
            self.animations[folder] = frames if frames else None

    # ← MÉTODO UPDATE CORREGIDO (AHORA SÍ EXISTE)
    def update(self, dt, puzzle_active=False):
        keys = pygame.key.get_pressed()

        new_pos = self.pos.copy()
        base_speed = 200
        move_speed = base_speed * dt
        moving = False
        
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.shadow_energy > 0:
            new_pos[0] -= move_speed
            self.facing = 'left'
            moving = True
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.shadow_energy > 0:
            new_pos[0] += move_speed
            self.facing = 'right'
            moving = True
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.shadow_energy > 0:
            new_pos[1] -= move_speed
            self.facing = 'back'
            moving = True
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.shadow_energy > 0:
            new_pos[1] += move_speed
            self.facing = 'front'
            moving = True

        # Colisiones
        player_rect = pygame.Rect(new_pos[0], new_pos[1], PIXEL_SCALE, PIXEL_SCALE)
        collision = any(player_rect.colliderect(obst) for obst in self.obstacles)
        if not collision:
            self.pos = new_pos

        # Ocultación
        self.hidden = keys[pygame.K_LSHIFT] and self.shadow_energy > 0
        if self.hidden:
            self.shadow_energy -= ENERGY_DRAIN_RATE * dt
        elif not puzzle_active and self.shadow_energy < self.max_shadow_energy:
            self.shadow_energy = min(self.max_shadow_energy, self.shadow_energy + self.energy_regen_rate * dt)

        # Límites
        self.pos[0] = max(0, min(self.pos[0], SCREEN_WIDTH - PIXEL_SCALE))
        self.pos[1] = max(0, min(self.pos[1], SCREEN_HEIGHT - PIXEL_SCALE))
        self.rect.topleft = self.pos

        # Animación
        anim_name = f"walk_{self.facing}" if moving else f"idle_{self.facing}"
        if anim_name != self.current_anim:
            self.current_anim = anim_name
            self.frame_idx = 0
            self.anim_timer = 0.0
        
        anim = self.animations.get(self.current_anim)
        if anim and len(anim) > 1:
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer -= self.frame_duration
                self.frame_idx = (self.frame_idx + 1) % len(anim)

    def draw(self, screen):
        anim = self.animations.get(self.current_anim)
        if not anim or not anim[self.frame_idx]:
            color = (0, 50, 128) if self.hidden else BLUE_PLAYER
            pygame.draw.rect(screen, color, self.rect)
        else:
            frame = anim[self.frame_idx]
            if self.hidden:
                hidden_frame = frame.copy()
                hidden_frame.fill((25, 25, 55), special_flags=pygame.BLEND_MULT)
                screen.blit(hidden_frame, self.rect)
            else:
                screen.blit(frame, self.rect)

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def add_energy(self, amount):
        self.shadow_energy = min(self.max_shadow_energy, self.shadow_energy + amount)

    def add_max_energy(self, amount):
        self.max_shadow_energy += amount
        self.shadow_energy = self.max_shadow_energy