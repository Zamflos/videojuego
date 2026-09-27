# main.py → VERSIÓN FINAL QUE SÍ FUNCIONA (la buena de verdad)
import pygame
from constants import *
from menu import title_screen, show_instructions, show_controls
from game import run_game

pygame.init()

info = pygame.display.Info()
REAL_WIDTH = info.current_w
REAL_HEIGHT = info.current_h
#REAL_WIDTH = 800  # En lugar de info.current_w
#REAL_HEIGHT = 600  # En lugar de info.current_h
screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT)

, pygame.NOFRAME)
pygame.event.pump()
pygame.time.delay(500)  # 0.5 seg para que el display se estabilice
pygame.display.set_caption("Secuencia Sombría")
#pygame.mouse.set_visible(False)

virtual_screen = pygame.Surface((800, 600))
clock = pygame.time.Clock()

def draw_scaled(virtual_surface, real_screen):
    scaled = pygame.transform.smoothscale(virtual_surface, (REAL_WIDTH, REAL_HEIGHT))
    real_screen.blit(scaled, (0, 0))
    pygame.display.flip()

# ==================== BUCLE PRINCIPAL ====================
running = True
while running:
    # ← ¡AQUÍ ESTÁ LA CLAVE! Llamamos UNA SOLA VEZ a cada menú
    action = title_screen(virtual_screen, clock, draw_scaled, screen)

    print(f"Acción seleccionada: {action}")
    if action == "play":
        print("Entrando en el bucle del juego...")
    if action == "quit":
        running = False
        break

    elif action == "play":
        while True:
            result = run_game(virtual_screen, clock, screen, draw_scaled)
            if result == "quit":
                running = False
                break
            elif result == "restart":
                continue  # vuelve a run_game()
            elif result == "menu":
                break     # vuelve al título

    elif action == "instructions":
        show_instructions(virtual_screen, clock, draw_scaled, screen)

    elif action == "controls":
        show_controls(virtual_screen, clock, draw_scaled, screen)

pygame.mouse.set_visible(True)
pygame.quit()