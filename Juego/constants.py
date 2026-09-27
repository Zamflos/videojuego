import pygame

# Initialize Pygame and font module
pygame.init()
pygame.font.init()

# Colores (paleta pixel art para ciudad apocalíptica)
PAVEMENT = (105, 105, 105)  # Pavimento gris agrietado
DRY_GRASS = (160, 82, 45)  # Pasto seco (marrón desvaído)
GRAY_RUINS = (80, 80, 80)  # Pavimento o tierra devastada
BROWN_CRACKED_STREET = (100, 50, 20)  # Calle agrietada
BLUE_PLAYER = (0, 100, 255)  # Jugador
RED_ENEMY = (200, 0, 0)  # Enemigo
YELLOW_FRAGMENT = (255, 255, 100)  # Fragmento
WHITE_TEXT = (255, 255, 255)  # Textos
GREEN_SUCCESS = (0, 200, 0)  # Éxito
ORANGE_ALERT = (255, 150, 0)  # Alerta
DARK_GRAY_BUILDINGS = (50, 50, 50)  # Edificios destruidos
LIGHT_GRAY = (150, 150, 150)  # Área de luz sutil
FIRE_RED = (255, 69, 0)  # Rojo fuego base
FIRE_ORANGE = (255, 165, 0)  # Naranja para animación de fuego
GREEN_POWERUP = (0, 255, 0)  # Color base del power-up
PURPLE_LORE = (128, 0, 128)  # Color para lore
BLUE_UPGRADE = (0, 0, 255)  # Color para mejoras

# Configuraciones
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PIXEL_SCALE = 16  # Tamaño base para pixel art
PLAYER_SPEED = 10
ENEMY_SPEED = 150  # +50%, más amenazantes
DETECTION_RANGE = 80
PUZZLE_RANGE = 40
POWER_UP_RANGE = 30
FONT = pygame.font.SysFont("monospace", 16)  # Fuente retro
ACTIONS = ['1', '2', '3']  # Acciones numéricas
ACTION_MAP = {
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3'
}
ENERGY_REGEN_RATE = 22
ENERGY_DRAIN_RATE = 30
HEALTH_DRAIN_RATE = 20
PUZZLE_TIME_LIMIT = 12
POWER_UP_COOLDOWN = 20.0 # Aumentado para no ser constantes
HEALTH_THRESHOLD = 30  # Umbral para ajustar dificultad
MAX_ENERGY = 100  # Máxima energía inicial
ENERGY_BOOST = 5  # Incremento en regeneración
CRATE_HINT_CHANCE = 30

# Luz radial (ajustado para tinte amarillento)
LIGHT_RADIUS_BASE = 100  # Radio inicial en píxeles
LIGHT_RADIUS_PER_FRAGMENT = 50  # Crecimiento por fragmento
MIN_LIGHT_BASE = 50  # Brillo mínimo inicial (oscuro)
MIN_LIGHT_PER_FRAGMENT = 40  # Incremento de brillo por fragmento (reduce oscuridad global)
LIGHT_COLOR_CENTER = (255, 255, 200)  # Amarillo claro (centro, como amanecer)
LIGHT_COLOR_EDGE = (255, 200, 100)  # Anaranjado (borde)

import math  # ← Para ceil en puzzles
CRATE_HINT_CHANCE = 30
ENEMY_DAMAGE_COOLDOWN = 0.2  # Ya debería estar, sino agrega

# Colores para visualización de secuencia puzzle
# === COLORES PARA LA VISUALIZACIÓN DEL PUZZLE ===
ACTION_COLORS = {
    '1': (50, 150, 255),    # Azul claro para 1
    '2': (50, 255, 100),    # Verde claro para 2
    '3': (255, 180, 50)     # Naranja cálido para 3
}
MAX_SHADOW_ENERGY = 100  # Valor máximo fijo para energía de sombra