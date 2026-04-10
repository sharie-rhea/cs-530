"""
Game constants, configuration, and global settings.

This module contains all game configuration values, including screen dimensions,
speeds, spawn rates, scoring values, and color definitions.
"""

# ============================================================================
# SCREEN AND DISPLAY SETTINGS
# ============================================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


# ============================================================================
# GAME MECHANICS SETTINGS
# ============================================================================

# Player settings
PLAYER_SPEED = 7

# Bullet settings
BULLET_SPEED = 10

# Enemy settings
ENEMY_BASE_SPEED = 2
ENEMY_SPAWN_RATE = 2  # Enemies per second
ASTEROID_BASE_SPEED = 1.5

# Game progression
MAX_HEALTH = 3
WAVE_SIZE = 5  # Enemies per wave
TOTAL_WAVES = 5

# Player invincibility
INVINCIBLE_DURATION = 120  # frames (2 seconds at 60 FPS)


# ============================================================================
# SCORING SYSTEM
# ============================================================================

POINTS_ASTEROID = 10
POINTS_ENEMY = 25
POINTS_WAVE_BONUS = 50


# ============================================================================
# FONT SIZES
# ============================================================================

FONT_LARGE = 48
FONT_MEDIUM = 32
FONT_SMALL = 24


# ============================================================================
# COLOR DEFINITIONS (RGB)
# ============================================================================

class Colors:
    """Color constants for the game."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    GRAY = (128, 128, 128)
