# game.py → VERSIÓN FINAL CON DERROTA + VICTORIA + TODO FUNCIONANDO
import pygame
import random
import math
from constants import *
from player import Player
from enemy import Enemy
from puzzle import Puzzle
from ui import UI
from objects import WorldObject
from menu import pause_menu, mouse_to_virtual 

# =============================================
# ESCALADO DE CAMINOS (32x32)
# =============================================
ROAD_SCALE = 5
ROAD_SIZE = PIXEL_SCALE * ROAD_SCALE  # 32x32

def load_road_tiles():
    try:
        straight_h = pygame.image.load('Sprites/roads/1.png').convert_alpha()
        straight_h = pygame.transform.scale(straight_h, (ROAD_SIZE, ROAD_SIZE))
    except:
        straight_h = pygame.Surface((ROAD_SIZE, ROAD_SIZE))
        straight_h.fill((100, 50, 20))

    try:
        curve = pygame.image.load('Sprites/roads/2.png').convert_alpha()
        curve = pygame.transform.scale(curve, (ROAD_SIZE, ROAD_SIZE))
    except:
        curve = pygame.Surface((ROAD_SIZE, ROAD_SIZE))
        curve.fill((120, 60, 30))

    return straight_h, curve

def rotate_tile(tile, angle):
    rotated = pygame.transform.rotate(tile, angle)
    new_surf = pygame.Surface((ROAD_SIZE, ROAD_SIZE), pygame.SRCALPHA)
    rect = rotated.get_rect(center=(ROAD_SIZE//2, ROAD_SIZE//2))
    new_surf.blit(rotated, rect.topleft)
    return new_surf

def initialize_environment():
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((20, 20, 20))

    # Césped seco
    for _ in range(12):
        x = random.randint(0, SCREEN_WIDTH - PIXEL_SCALE * 5)
        y = random.randint(0, SCREEN_HEIGHT - PIXEL_SCALE * 5)
        w = random.randint(PIXEL_SCALE * 3, PIXEL_SCALE * 6)
        h = random.randint(PIXEL_SCALE * 3, PIXEL_SCALE * 6)
        pygame.draw.rect(background, DRY_GRASS, (x, y, w, h))

    straight_h, curve = load_road_tiles()
    straight_v = rotate_tile(straight_h, 90)
    curve_tr = curve

    tile = ROAD_SIZE

    # Camino horizontal arriba
    for x in range(0, SCREEN_WIDTH, tile):
        background.blit(straight_h, (x, 120))

    # Camino vertical + curva
    x_vert = 380
    for y in range(0, 400 + tile, tile):
        background.blit(straight_v, (x_vert, y))

    background.blit(curve_tr, (x_vert, 400))

    for x in range(x_vert + tile, x_vert + tile * 15, tile):
        background.blit(straight_h, (x, 400))

    return background

def apply_light(screen, player, puzzle):
    progress = min(1.0, puzzle.fragments / 1)
    radius = int(LIGHT_RADIUS_BASE + progress * 5 * LIGHT_RADIUS_PER_FRAGMENT)
    light_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    if progress >= 1.0:
        light_surf.fill((255, 255, 255, 255))
    else:
        cx = int(player.pos[0] + PIXEL_SCALE // 2)
        cy = int(player.pos[1] + PIXEL_SCALE // 2)
        for i in range(0, radius, 10):
            alpha = int(130 * (1 - i / radius))
            r = int(LIGHT_COLOR_CENTER[0] * (1 - i / radius) + LIGHT_COLOR_EDGE[0] * (i / radius))
            g = int(LIGHT_COLOR_CENTER[1] * (1 - i / radius) + LIGHT_COLOR_EDGE[1] * (i / radius))
            b = int(LIGHT_COLOR_CENTER[2] * (1 - i / radius) + LIGHT_COLOR_EDGE[2] * (i / radius))
            pygame.draw.circle(light_surf, (r, g, b, alpha), (cx, cy), radius - i)
    screen.blit(light_surf, (0, 0), special_flags=pygame.BLEND_MULT)

# === PANTALLA DE DERROTA ===
def defeat_screen(virtual_screen, clock, draw_scaled, screen, background, world_objects, enemies, player):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))
    fade.set_alpha(200)

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key in (pygame.K_ESCAPE, pygame.K_m):
                    return "menu"

        # Fondo congelado
        virtual_screen.blit(background, (0, 0))
        for obj in world_objects:
            if obj.active:
                obj.draw(virtual_screen)
        for e in enemies:
            e.draw(virtual_screen)
        player.draw(virtual_screen)

        virtual_screen.blit(fade, (0, 0))

        # Texto DERROTA
        font_big = pygame.font.SysFont("monospace", 50, bold=True) 
        text = font_big.render("consumido por la oscuridad", True, (200, 0, 0))  # ← Aquí está el texto
        shadow = font_big.render("consumido por la oscuridad", True, (100, 0, 0))  
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)) 
        virtual_screen.blit(shadow, (rect.x+5, rect.y+5)) 
        virtual_screen.blit(text, rect)

        font_small = pygame.font.SysFont("monospace", 30)
        inst = font_small.render("R → Reiniciar    ESC / M → Menú Principal", True, (200, 200, 200))
        virtual_screen.blit(inst, inst.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))

        draw_scaled(virtual_screen, screen)

# === PANTALLA DE VICTORIA (mejorada) ===
# === PANTALLA DE VICTORIA MEJORADA (copia pero elegante) ===
# === PANTALLA DE VICTORIA FINAL - ELEGANTE Y PERFECTA ===
# === PANTALLA DE VICTORIA - ESTILO RETRO LIMPIO (SIN AMARILLO) ===
def victory_screen(virtual_screen, clock, draw_scaled, screen, background, world_objects, enemies, player):
    title_text = "VICTORIA"
    displayed = ""
    char_index = 0
    type_timer = 0.0
    type_speed = 0.09

    # Empieza en el centro exacto de la pantalla
    title_y = SCREEN_HEIGHT // 2
    title_speed = 60  # píxeles por segundo hacia arriba

    credits_y = SCREEN_HEIGHT + 100
    show_credits = False  # Los créditos empiezan después

    credits_lines = [
        "", "", "", "", "",
        "DESARROLLADO POR",
        "Malcom Flores",
        "Jose Angel tapia",
        "Marcos Castro",
        "Diego Marcus Caldera",
        "Con ayuda de el gran asistente",
        "GROK",
        "",
        "Gracias por jugar",
        "esta tremenda beta",
        "",
        "El sol ha regresado.",
        "",
        "R  →  Jugar de nuevo",
        "ESC / M  →  Menú principal",
        "", "", "", "", "",
    ]

    font_title = pygame.font.SysFont("monospace", 130, bold=True)
    font_credits = pygame.font.SysFont("monospace", 36)

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key in (pygame.K_ESCAPE, pygame.K_m):
                    return "menu"

        # Fondo del juego tal como quedó al ganar
        virtual_screen.blit(background, (0, 0))
        for obj in world_objects:
            if obj.active:
                obj.draw(virtual_screen)
        for e in enemies:
            e.draw(virtual_screen)
        player.draw(virtual_screen)

        # === VICTORIA: aparece letra por letra en el centro ===
        if char_index < len(title_text):
            type_timer += dt
            if type_timer >= type_speed:
                displayed += title_text[char_index]
                char_index += 1
                type_timer = 0

        # === Una vez escrito todo, empieza a subir ===
        if char_index >= len(title_text):
            title_y -= title_speed * dt
            # Cuando llega arriba del todo, activamos los créditos
            if title_y <= 150 and not show_credits:
                show_credits = True

        # Dibujar título con sombra negra
        if displayed:
            surf = font_title.render(displayed, True, (255, 255, 255))
            shadow = font_title.render(displayed, True, (0, 0, 0))
            rect = surf.get_rect(center=(SCREEN_WIDTH//2, title_y))
            virtual_screen.blit(shadow, (rect.x + 8, rect.y + 8))
            virtual_screen.blit(surf, rect)

        # === CRÉDITOS: suben desde abajo (solo cuando el título ya subió) ===
        if show_credits:
            credits_y -= 45 * dt
            for i, line in enumerate(credits_lines):
                y = credits_y + i * 55
                if -100 < y < SCREEN_HEIGHT + 100:
                    alpha = int(255 * (1 - abs(y - SCREEN_HEIGHT//2) / 600))
                    alpha = max(40, min(255, alpha))
                    color = (255, 255, 255) if line.strip() and line.strip() in ["Malcom", "GROK", "GRACIAS POR JUGAR"] else (200, 200, 200)
                    txt = font_credits.render(line, True, color)
                    txt.set_alpha(alpha)
                    virtual_screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH//2, y)))

        draw_scaled(virtual_screen, screen)

# === FUNCIÓN PRINCIPAL DEL JUEGO ===
def run_game(virtual_screen, clock, screen, draw_scaled):
    print("Iniciando partida...")

    background = initialize_environment()
    player = Player()
    puzzle = Puzzle()
    ui = UI()
    active_messages = []

    # === OBJETOS DEL MUNDO ===
    world_objects = []
    for _ in range(14):
        while True:
            x = random.randint(40, SCREEN_WIDTH - 100)
            y = random.randint(40, SCREEN_HEIGHT - 100)
            if 100 <= y <= 160: continue
            if 360 <= x <= 440 and y <= 480: continue
            break
        scale = random.uniform(1.3, 2.4)
        world_objects.append(WorldObject('wall', (x, y), scale=scale))

    for _ in range(6):
        world_objects.append(WorldObject('crate', (random.randint(30, SCREEN_WIDTH - 80), random.randint(30, SCREEN_HEIGHT - 80))))
    for _ in range(4):
        world_objects.append(WorldObject('campfire', (random.randint(60, SCREEN_WIDTH - 100), random.randint(60, SCREEN_HEIGHT - 100))))
    for _ in range(3):
        while True:
            x = random.randint(40, SCREEN_WIDTH - 100)
            y = random.randint(40, SCREEN_HEIGHT - 100)
            if 100 <= y <= 160: continue
            if 360 <= x <= 440 and y <= 480: continue
            break
        world_objects.append(WorldObject('health_pack', (x, y)))

    player.obstacles = [obj.rect for obj in world_objects if obj.type == 'wall']
    
    # === ENEMIGOS ===
    enemies = [Enemy(player.obstacles) for _ in range(5)]

    # Timers
    damage_timer = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    btns = pause_menu(virtual_screen, [])
                    paused = True
                    while paused:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                return "quit"
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                                paused = False
                            if e.type == pygame.MOUSEBUTTONDOWN:
                                mx, my = mouse_to_virtual(e.pos, screen)
                                if btns[0].collidepoint(mx, my):
                                    paused = False
                                if btns[1].collidepoint(mx, my):
                                    return "restart"
                                if btns[2].collidepoint(mx, my):
                                    return "menu"
                                if btns[3].collidepoint(mx, my):
                                    return "quit"
                        virtual_screen.blit(background, (0, 0))
                        for obj in world_objects:
                            if obj.active: obj.draw(virtual_screen)
                        for e in enemies: e.draw(virtual_screen)
                        player.draw(virtual_screen)
                        pause_menu(virtual_screen, [])
                        draw_scaled(virtual_screen, screen)

                # Interacción con objetos
                if event.key == pygame.K_e:
                    for obj in world_objects:
                        item = obj.interact(player.pos)
                        if item == 'energy':
                            player.add_energy(30)
                            ui.show_message("+30 Energía", (0, 255, 255), active_messages)
                        elif item == 'health':
                            player.health = min(100, player.health + 40)
                            ui.show_message("+40 Vida", (0, 255, 0), active_messages)
                        elif item == 'hint':
                            ui.show_partial_hint(puzzle.current_sequence, active_messages)
                        elif item == 'fragment':
                            puzzle.fragments += 1
                            ui.show_message("¡Fragmento encontrado!", YELLOW_FRAGMENT, active_messages)
                        elif item == 'light_boost':
                            player.add_max_energy(20)
                            ui.show_message("¡Fuego eterno! +20 energía máxima", (255, 165, 0), active_messages)

                # Puzzle input
                result, player.health = puzzle.handle_input(event, player.health)
                if result == "fail":
                    player.take_damage(20)
                    ui.show_message("¡Fallaste! -20 vida", (255, 0, 0), active_messages)
                elif result == "success":
                    ui.show_message("¡Correcto! Fragmento +1", (0, 255, 0), active_messages)

        # === ACTUALIZACIONES ===
        player.update(dt, puzzle.active)
        for obj in world_objects:
            obj.update(dt, player.pos)
        for e in enemies:
            e.update(dt)

        puzzle_result, _ = puzzle.update(dt)
        if puzzle_result == "timeout":
            player.take_damage(20)
            ui.show_message("¡Tiempo agotado! -20 vida", (255, 100, 0), active_messages)

        # Daño por enemigos
        if any(e.detect(player) for e in enemies):
            if damage_timer <= 0:
                player.take_damage(HEALTH_DRAIN_RATE * dt * 30)  # Daño más constante
                damage_timer = ENEMY_DAMAGE_COOLDOWN
            else:
                damage_timer -= dt

        # === COMPROBAR DERROTA ===
        if player.health <= 0:
            return defeat_screen(virtual_screen, clock, draw_scaled, screen, background, world_objects, enemies, player)

        # === COMPROBAR VICTORIA ===
        if puzzle.fragments >= 5:
            return victory_screen(virtual_screen, clock, draw_scaled, screen, background, world_objects, enemies, player)
         # === DIBUJADO ===
        virtual_screen.blit(background, (0, 0))

        for obj in world_objects:
            if obj.active:
                obj.draw(virtual_screen)

        for e in enemies:
            e.draw(virtual_screen)

        player.draw(virtual_screen)

        if not puzzle.active and puzzle.fragments < 5:
            puzzle.draw_fragment(virtual_screen)

        if puzzle.check_activation(player.pos):
            ui.show_message("¡Secuencia detectada! Usa teclas 1-2-3", (255, 255, 0), active_messages)

        apply_light(virtual_screen, player, puzzle)
        ui.draw(virtual_screen, player, puzzle, alert=any(e.detect(player) for e in enemies))

        # Mensajes flotantes
        for msg in active_messages[:]:
            msg["remaining_time"] -= dt
            text = FONT.render(msg["text"], True, msg["color"])
            rect = text.get_rect(center=(SCREEN_WIDTH//2, 80 + active_messages.index(msg)*30))
            virtual_screen.blit(text, rect)
            if msg["remaining_time"] <= 0:
                active_messages.remove(msg)

        draw_scaled(virtual_screen, screen)

    return "menu"