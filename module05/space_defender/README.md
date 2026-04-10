# Space Defender - 2D Arcade Game

A classic space shooter arcade game built with Python and Pygame. Destroy waves of asteroids and enemy ships while protecting your spaceship!

## Overview

**Space Defender** is a 2D arcade-style game where players control a spaceship at the bottom of the screen, moving left and right to dodge incoming asteroids and enemy ships while firing bullets to destroy them. The game features progressively more challenging waves of enemies and a comprehensive scoring system.

## Features

✅ **2D Graphics**: Colorful vector-based sprite designs using pygame  
✅ **Keyboard Controls**: ARROW KEYS or A/D to move, SPACE to fire  
✅ **Challenge Mechanic**: Wave-based enemy system with increasing difficulty  
✅ **Scoring System**: Points for asteroids (+10), enemy ships (+25), powerups (+50), and wave bonuses (+50)  
✅ **On-Screen Instructions**: Clear gameplay instructions and controls displayed  
✅ **Win/Lose Conditions**: 3 health points system and complete 5 waves to win  
✅ **Powerup System**: Rapid fire and invincibility powerups drop from defeated enemies  
✅ **HUD**: Real-time display of score, health, and current wave number  

## Requirements

- Python 3.8+
- pygame

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   pip install pygame
   ```

## Running the Game

Execute the following command in the project directory:

```bash
python space_defender.py
```

## How to Play

### Controls
- **LEFT ARROW** or **A**: Move spaceship left
- **RIGHT ARROW** or **D**: Move spaceship right
- **SPACE**: Fire bullets
- **ESC**: Pause/Resume game (during gameplay)
- **M**: Return to menu from pause screen
- **ESC**: Quit game from main menu

### Game Mechanics

1. **Waves**: The game consists of 5 waves. Each wave spawns progressively more enemies.
2. **Enemies**: 
   - **Asteroids** (Gray, worth +10 points): Rotate and move downward
   - **Enemy Ships** (Red, worth +25 points): Move with randomized path patterns toward your position
3. **Enemy Attacks** (Waves 3+): Enemy ships begin firing red projectiles toward you
4. **Health**: You start with 3 health points. Colliding with any enemy or taking enemy fire costs 1 health.
5. **Invincibility Frames**: After taking damage, you have 2 seconds of invincibility (blinking effect).
6. **Powerups**: Defeated enemies have a chance to drop powerups:
   - **Rapid Fire** (Yellow star): Fire a rapid stream of bullets while holding SPACE
   - **Invincibility** (Cyan shield): Gain 5 seconds of damage protection
7. **Scoring**:
   - Destroy an asteroid: +10 points
   - Destroy an enemy ship: +25 points
   - Collect a powerup: +50 points
   - Complete a wave: +50 bonus points

### Win/Lose Conditions

**Lose**: Your health reaches 0 (take 3 hits)  
**Win**: Successfully survive and destroy all enemies in all 5 waves

## Game States

1. **Menu**: Main menu with instructions. Press SPACE to start or ESC to quit.
2. **Playing**: Main gameplay. Defeat all enemies in the current wave. Press ESC to pause. Wave start message appears at the beginning of each wave.
3. **Paused**: Game paused with overlay menu. Press ESC to resume or M to return to menu.
4. **Game Over**: Game ended due to lost health. Press SPACE to return to menu.
5. **Won**: Successfully completed all 5 waves. Press SPACE to return to menu.

## Code Architecture

### File Structure
```
space_defender.py          # Entry point - runs the game
constants.py              # All game configuration and constants
game_state.py             # GameState enum for state management
entities.py               # Player, Bullet, Asteroid, EnemyShip, Powerup classes
game.py                   # SpaceDefenderGame main class
README.md                 # This file
requirements.txt          # Python dependencies
```

### Module Breakdown

**space_defender.py** - Entry Point
- Simple `main()` function that initializes and runs the game
- Clean, minimal interface to launch gameplay

**constants.py** - Configuration & Constants
- Screen dimensions (800x600)
- Game mechanics (speeds, spawn rates, health)
- Scoring values (points per enemy type)
- Color definitions (RGB tuples)
- Font sizes
- All settings easily adjustable in one place

**game_state.py** - State Management
- `GameState` enum: MENU, PLAYING, PAUSED, GAME_OVER, GAME_WON
- Type-safe state system for game flow control

**entities.py** - Game Entities
- `Player`: Spaceship with movement, firing, and powerup mechanics
- `Bullet`: Projectile class for player and enemy shots
- `Asteroid`: Rotating asteroid enemies with random shapes
- `EnemyShip`: Intelligent enemies that track player and shoot in higher waves
- `Powerup`: Power-up items dropped by defeated enemies (rapid fire, invincibility)
- Each class handles its own rendering and physics

**game.py** - Game Engine
- `SpaceDefenderGame`: Main game loop and management
- Event handling and input processing
- Entity updates and physics
- Collision detection system
- Game state transitions
- Rendering and HUD display

### Design Benefits

- **Modularity**: Each file has a single, well-defined purpose
- **Maintainability**: Related code grouped logically
- **Scalability**: Easy to add new entity types or mechanics
- **Testability**: Individual modules can be tested independently
- **Readability**: Smaller files are easier to understand
- **Reusability**: Constants and utilities can be used by extensions

## Game Balance Settings

You can adjust game difficulty by modifying these constants in `space_defender.py`:

- `PLAYER_SPEED`: How fast the player moves (default: 7)
- `BULLET_SPEED`: How fast bullets travel (default: 10)
- `ENEMY_BASE_SPEED`: Base speed of asteroids (default: 1.5)
- `ENEMY_SPAWN_RATE`: Enemies spawned per second (default: 2)
- `MAX_HEALTH`: Player health points (default: 3)
- `WAVE_SIZE`: Enemies per wave (default: 5)
- `TOTAL_WAVES`: Number of waves to complete (default: 5)

## Citations and Attribution

### Dependencies
- **Pygame**: https://www.pygame.org/
  - A cross-platform set of Python modules designed for writing video games
  - License: LGPL

### Design Inspiration
- Classic arcade shooters (Space Invaders, Galaga)
- Modern 2D game design patterns

### Code Standards
- PEP 8 Python style guide compliance
- Type hints for improved code clarity
- Comprehensive docstrings for all classes and methods
- Well-organized class structure with clear separation of concerns

## Technical Details

### Collision Detection
Uses circular bounding box collision detection for performance and simplicity. Each entity has a radius calculated from its sprite dimensions.

### Game Loop
The game runs at 60 FPS with:
1. Event handling (keyboard input)
2. Game state updates (entity movement, collisions)
3. Rendering (drawing all entities and UI)

### Performance Optimization
- Sprite pooling for bullets, asteroids, and enemies
- Offscreen entity removal to prevent memory bloat
- Efficient collision detection using spatial proximity

## Troubleshooting

**Game won't start:**
- Ensure pygame is installed: `pip install pygame`
- Check Python version is 3.8 or higher

**Low frame rate:**
- Close other applications
- Reduce visual effects by lowering FPS cap (not recommended)

**Controls not responding:**
- Ensure the game window has focus
- Try alternative movement keys (A/D instead of arrows)

## Future Enhancement Ideas

- Sound effects and background music
- Additional powerup types (shield, slowdown, extra health)
- Multiple difficulty levels
- Leaderboard system
- Different enemy types with special abilities
- Boss battles
- Particle effects for explosions
- Multiplayer mode

## Author

Created for educational purposes in an AI and Software Engineering course.  
Date: March 2026

## License

This project serves educational purposes. Pygame is distributed under the LGPL license.
