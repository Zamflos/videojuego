# menu.py → VERSIÓN 100% COMPLETA Y FUNCIONAL (incluye pause_menu)
import pygame
from constants import *

def draw_text(screen, font, text, color, x, y, center=True):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

# Convierte coordenadas reales → virtuales (800×600)
def mouse_to_virtual(pos, real_screen):
    real_w, real_h = real_screen.get_size()
    return (
        int(pos[0] * SCREEN_WIDTH  / real_w),
        int(pos[1] * SCREEN_HEIGHT / real_h)
    )

def title_screen(virtual_screen, clock, draw_scaled, screen):
    font_big = pygame.font.SysFont("monospace", 80, bold=True)
    font_med = pygame.font.SysFont("monospace", 40)
    
    btn_play  = pygame.Rect(SCREEN_WIDTH//2 - 150, 300, 300, 80)
    btn_inst  = pygame.Rect(SCREEN_WIDTH//2 - 150, 400, 300, 80)
    btn_ctrl  = pygame.Rect(SCREEN_WIDTH//2 - 150, 500, 300, 80)
    btn_quit  = pygame.Rect(SCREEN_WIDTH//2 - 150, 600, 300, 80)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "play"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = mouse_to_virtual(event.pos, screen)
                if btn_play.collidepoint(mx, my):
                    return "play"
                if btn_inst.collidepoint(mx, my):
                    return "instructions"
                if btn_ctrl.collidepoint(mx, my):
                    return "controls"
                if btn_quit.collidepoint(mx, my):
                    return "quit"

        # Dibujar menú
        virtual_screen.fill((10, 10, 20))
        title = font_big.render("SECUENCIA SOMBRÍA", True, (0, 200, 255))
        virtual_screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 150)))

        for rect, text, color in [
            (btn_play,  "JUGAR",         (0, 200, 0)),
            (btn_inst,  "INSTRUCCIONES", (0, 150, 255)),
            (btn_ctrl,  "CONTROLES",     (255, 150, 0)),
            (btn_quit,  "SALIR",         (200, 0, 0))
        ]:
            pygame.draw.rect(virtual_screen, color, rect, border_radius=15)
            pygame.draw.rect(virtual_screen, (255,255,255), rect, 4, border_radius=15)
            txt = font_med.render(text, True, (255,255,255))
            virtual_screen.blit(txt, txt.get_rect(center=rect.center))

        small = pygame.font.SysFont("monospace", 20).render("ENTER o clic → JUGAR   ESC → Salir", True, (100,100,100))
        virtual_screen.blit(small, small.get_rect(center=(SCREEN_WIDTH//2, 680)))

        clock.tick(60)
        draw_scaled(virtual_screen, screen)

def show_instructions(virtual_screen, clock, draw_scaled, screen):  # ← Sin events
    while True:
        for event in pygame.event.get():  # ← Siempre obtener eventos nuevos
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "quit"
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

        virtual_screen.fill((15, 15, 30))
        lines = [
            "HISTORIA",
            "Eres el último portador de luz en una ciudad",
            "devorada por la oscuridad eterna.",
            "Los Fragmentos de Amanecer son la única esperanza",
            "para restaurar el sol.",
            "",
            "OBJETIVO",
            "Recoge los 5 Fragmentos de Amanecer resolviendo",
            "secuencias numéricas antes de que se acabe el tiempo.",
            "",
            "¡Usa las sombras para ocultarte y sobrevivir!",
            "",
            "Clic o cualquier tecla para volver",
            "",
            "",
            "Malcom, Jose Angel, Diego Marcus, Marcos",
        ]
        y = 70
        for line in lines:
            if not line:
                y += 25
                continue
            font = pygame.font.SysFont("monospace", 28, bold=True) if "HISTORIA" in line or "OBJETIVO" in line else pygame.font.SysFont("monospace", 20)
            color = (0, 200, 255) if "HISTORIA" in line or "OBJETIVO" in line else WHITE_TEXT
            draw_text(virtual_screen, font, line, color, SCREEN_WIDTH//2, y)
            y += 34 if "HISTORIA" in line or "OBJETIVO" in line else 28

        clock.tick(60)
        draw_scaled(virtual_screen, screen)

def show_controls(virtual_screen, clock, draw_scaled, screen):  # ← Sin events
    while True:
        for event in pygame.event.get():  # ← Siempre obtener eventos nuevos
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "quit"
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

        virtual_screen.fill((15, 15, 30))
        y = 80 
        draw_text(virtual_screen, pygame.font.SysFont("monospace", 32, bold=True), "CONTROLES", (0, 220, 255), SCREEN_WIDTH//2, y)
        y += 70
        controls = [
            ("W A S D "  , "Moverse"),
            ("SHIFT"           , "Ocultarse en sombras"),
            ("1 · 2 · 3"       , "Resolver secuencia"),
            ("E"               , "Interactuar con objetos"),
            ("ESC"             , "Pausar / Volver"),
        ]
        for key, desc in controls:
            draw_text(virtual_screen, pygame.font.SysFont("monospace", 24, bold=True), key, (0, 200, 255), 220, y, center=False)
            draw_text(virtual_screen, pygame.font.SysFont("monospace", 20), desc, WHITE_TEXT, 380, y, center=False)
            y += 40 
        draw_text(virtual_screen, pygame.font.SysFont("monospace", 18), "Clic o tecla para volver", (180,180,180), SCREEN_WIDTH//2, SCREEN_HEIGHT-60)

        clock.tick(60)
        draw_scaled(virtual_screen, screen)

# ← ¡¡AQUÍ ESTÁ LA FUNCIÓN QUE FALTABA!!
def pause_menu(virtual_screen, events):  # ← Mantiene events, se llama por frame en game.py
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(140)
    overlay.fill((0, 0, 0))
    virtual_screen.blit(overlay, (0, 0))

    draw_text(virtual_screen, pygame.font.SysFont("monospace", 56, bold=True), "PAUSADO", (200, 200, 255), SCREEN_WIDTH//2, 150)

    bw, bh = 280, 60
    y0 = 250
    btns = [pygame.Rect(SCREEN_WIDTH//2 - bw//2, y0 + i*(bh+25), bw, bh) for i in range(4)]
    texts = ["REANUDAR", "REINICIAR", "MENÚ PRINCIPAL", "SALIR"]
    colors = [(0, 180, 0), (255, 140, 0), (140, 0, 255), (200, 0, 0)]

    for btn, txt, col in zip(btns, texts, colors):
        pygame.draw.rect(virtual_screen, col, btn, border_radius=12)
        pygame.draw.rect(virtual_screen, (255, 255, 255, 80), btn, 4, border_radius=12)
        draw_text(virtual_screen, pygame.font.SysFont("monospace", 32, bold=True), txt, WHITE_TEXT, btn.centerx, btn.centery)

    return btns  # Devuelve los rects para detectar clics en game.py