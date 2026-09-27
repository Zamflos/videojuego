# enemy.py → Versión FINAL con sprite + método detect() CORREGIDO
import pygame
import math
import random
from constants import *

class Enemy:
    def __init__(self, obstacles):
        self.pos = [600, 200]
        self.direction = [0, 0]
        self.speed = ENEMY_SPEED
        self.obstacles = obstacles
        self.paused = False
        self.pause_timer = 0
        self.pause_duration = 0

        # CARGAR SPRITE DEL ENEMIGO
        try:
            img = pygame.image.load('Sprites/enemy/enemy.png').convert_alpha()
            self.image = pygame.transform.scale(img, (PIXEL_SCALE, PIXEL_SCALE))
        except Exception as e:
            print(f"[ERROR] Sprite enemigo no encontrado: {e}")
            print("    → Usando rectángulo rojo como fallback")
            self.image = pygame.Surface((PIXEL_SCALE, PIXEL_SCALE))
            self.image.fill(RED_ENEMY)

        self.rect = self.image.get_rect()

    def update(self, dt):
        if not self.paused:
            # Posibles pausas aleatorias
            if random.random() < 0.05:
                self.paused = True
                self.pause_duration = random.uniform(1.5, 4.0)
                self.pause_timer = self.pause_duration

            # Dirección aleatoria si no tiene una
            if self.direction[0] == 0 and self.direction[1] == 0:
                angle = random.uniform(0, 2 * math.pi)
                self.direction = [math.cos(angle), math.sin(angle)]

            # Nueva posición tentativa
            new_pos = [
                self.pos[0] + self.direction[0] * self.speed * dt,
                self.pos[1] + self.direction[1] * self.speed * dt
            ]

            self.rect.topleft = new_pos
            collision = any(self.rect.colliderect(obst) for obst in self.obstacles)

            if not collision and 0 <= new_pos[0] <= SCREEN_WIDTH - PIXEL_SCALE and 0 <= new_pos[1] <= SCREEN_HEIGHT - PIXEL_SCALE:
                self.pos = new_pos
            else:
                # Rebote
                self.direction[0] *= -1
                self.direction[1] *= -1

        else:
            self.pause_timer -= dt
            if self.pause_timer <= 0:
                self.paused = False

    # ESTE MÉTODO FALTABA → SIN ÉL CRASHEA EL JUEGO
    def detect(self, player):
        dist = math.hypot(player.pos[0] - self.pos[0], player.pos[1] - self.pos[1])
        return not player.hidden and dist < DETECTION_RANGE

    def draw(self, screen):
        screen.blit(self.image, self.pos)

        # (Opcional) Círculo de detección para debug
        # pygame.draw.circle(screen, (255,0,0), 
        #                    (int(self.pos[0] + PIXEL_SCALE//2), int(self.pos[1] + PIXEL_SCALE//2)),
        #                    DETECTION_RANGE, 1)