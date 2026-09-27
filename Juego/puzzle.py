import random
import pygame
import math
from constants import *

class Puzzle:
    def __init__(self):
        self.fragment_pos = [100, 200]
        self.active = False
        self.current_sequence = []
        self.player_sequence = []
        self.length = 3.0  # ← Float desde init para +0.5 suave
        self.fragments = 0
        self.timer = 0

    def generate_sequence(self):
        self.length = max(3.0, self.length)  # Reset min
        seq_len = int(math.ceil(self.length))  # ← FIX: int ceil → 3.5=4, lento crecimiento
        self.current_sequence = random.choices(ACTIONS, k=seq_len)
        self.timer = PUZZLE_TIME_LIMIT

    def check_activation(self, player_pos):
        if self.fragments >= 5:  # No activar si ya se recogieron 5 fragmentos
            return False
        dist = math.hypot(player_pos[0] - self.fragment_pos[0], player_pos[1] - self.fragment_pos[1])
        if dist < PUZZLE_RANGE and not self.active:
            self.active = True
            self.generate_sequence()
            return True
        return False

    def update(self, dt):
        if self.active and self.fragments < 5:  # Actualizar solo si no se han recogido 5 fragmentos
            self.timer -= dt
            if self.timer <= 0:
                self.active = False
                self.player_sequence = []
                if self.fragments < 5:  # Generar nuevo fragmento solo si no se han recogido 5
                    self.fragment_pos = [random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)]
                return "timeout", 0  # No daño
        return None, 0

    def handle_input(self, event, player_health):
            if self.active and self.fragments < 5 and event.type == pygame.KEYDOWN:
                key = event.key
                if key in ACTION_MAP:
                    self.player_sequence.append(ACTION_MAP[key])
                    if len(self.player_sequence) > len(self.current_sequence):
                        self.player_sequence = []
                        if self.fragments < 5:
                            self.generate_sequence()
                        return "fail", player_health - 20
                    if len(self.player_sequence) == len(self.current_sequence):
                        if self.player_sequence == self.current_sequence:
                            self.fragments += 1
                            self.active = False
                            self.length = min(6.0, self.length + 0.5)  # ← +0.5 lento, float OK
                            if self.fragments < 5:
                                self.fragment_pos = [random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)]
                            self.player_sequence = []
                            return "success", player_health
                        else:
                            self.player_sequence = []
                            if self.fragments < 5:
                                self.generate_sequence()
                            return "fail", player_health - 20
            return None, player_health

    def draw_fragment(self, screen):
        if self.fragments < 5:  # Dibujar solo si no se han recogido 5 fragmentos
            pygame.draw.circle(screen, YELLOW_FRAGMENT, (self.fragment_pos[0] + PIXEL_SCALE // 2, self.fragment_pos[1] + PIXEL_SCALE // 2), PIXEL_SCALE // 2)