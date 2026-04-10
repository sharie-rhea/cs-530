"""
Game state management and enums.

This module contains the GameState enum for managing game flow.
"""

from enum import Enum


# ============================================================================
# GAME STATE ENUMS
# ============================================================================

class GameState(Enum):
    """Enumeration of possible game states."""
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    GAME_WON = 5
