"""
Space Defender - Entry Point
=============================

A classic space shooter game built with Pygame where players control a spaceship
to destroy incoming waves of asteroids and enemy ships.

This is the main entry point for the game. The game logic is organized
into separate modules for better maintainability:

- constants.py: Game configuration and constants
- game_state.py: Game state enums and utility classes
- entities.py: Player, Bullet, Asteroid, and EnemyShip classes
- game.py: Main SpaceDefenderGame class

Game Requirements Met:
1. 2D graphics using pygame
2. Keyboard input for game control
3. Challenge mechanic: Wave-based enemies with increasing difficulty
4. Functional scoring system with on-screen display
5. Visible player instructions on screen
6. Win/lose conditions with game over states

Author: Generated for educational purposes
Date: March 2026
Dependencies: pygame (https://www.pygame.org/)
"""

from game import SpaceDefenderGame


def main():
    """Initialize and run the game."""
    game = SpaceDefenderGame()
    game.run()


if __name__ == "__main__":
    main()
