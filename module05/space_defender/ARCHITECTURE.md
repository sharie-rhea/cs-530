# Project Structure Overview

## Modular Organization

The Space Defender project has been reorganized into separate, logical modules for better maintainability and scalability.

```
module05/
├── space_defender.py      ← ENTRY POINT (run this to play)
├── constants.py           ← Configuration & Constants
├── game_state.py          ← Enums & Utility Classes
├── entities.py            ← Game Entity Classes
├── game.py                ← Main Game Engine
├── README.md              ← Game Documentation
├── requirements.txt       ← Dependencies
└── ARCHITECTURE.md        ← This file
```

## Module Responsibilities

### 1. **constants.py** (70 lines)
**Purpose:** Centralized configuration hub
- Screen dimensions: `SCREEN_WIDTH`, `SCREEN_HEIGHT`
- Game mechanics: speeds, spawn rates, health
- Scoring system: points per enemy type
- Visual settings: font sizes, colors (RGB)

**Benefits:**
- Change difficulty in one place
- Experiment with balance settings easily
- No hunting through code for magic numbers

### 2. **game_state.py** (20 lines)
**Purpose**: State management and enums
- `GameState` enum: Controls game flow (MENU → PLAYING → PAUSED → GAME_OVER/WON)

**Benefits:**
- Type-safe state management
- Prevents invalid game transitions

### 3. **entities.py** (420 lines)
**Purpose:** All drawable game objects
- `Player`: Player spaceship (movement + firing)
- `Bullet`: Projectiles with customizable colors (yellow player, red enemy in waves 3+)
- `Asteroid`: Rotating asteroid enemies
- `EnemyShip`: AI enemies with randomized movement patterns and shooting (waves 3+)

**Key Features:**
- Enemy AI includes randomness for unpredictable movement
- Enemy ships can fire projectiles in higher difficulty waves
- Bullet class supports multiple colors for visual distinction

**Benefits:**
- Each class self-contained with own rendering/physics
- Easy to add new entity types
- Clear separation of entity behaviors
- Collision properties built-in

### 4. **game.py** (512 lines)
**Purpose**: Game engine and logic
- `SpaceDefenderGame`: Main game loop control
- Event handling (keyboard input processing including pause)
- Entity updates and physics calculations
- Collision detection engine (bullets, asteroids, enemies, enemy fire)
- Game state transitions (menu, playing, paused, win/lose/next wave)
- Rendering pipeline (HUD, entities, menus, wave start messages)

**Key Features:**
- Wave start announcement messages ("Wave X is starting...")
- Separate tracking for player bullets and enemy bullets
- Handles enemy bullet spawning based on wave difficulty
- Pause state with overlay menu
- Powerup collision detection and activation
- Per-wave enemy kill tracking

**Benefits:**
- Complete game flow in one place
- Easy to understand state transitions
- Modular rendering methods (_draw_menu, _draw_game, _draw_pause, etc.)
- Separated from entity definitions

### 5. **space_defender.py** (40 lines)
**Purpose:** Entry point and launcher
- `main()`: Initializes and runs the game
- Clean interface for external launch

**Benefits:**
- Simple to run: `python space_defender.py`
- Separates launcher from implementation
- Allows future integration (GUI launcher, etc.)

## Data Flow

```
INPUT (Keyboard)
    ↓
space_defender.py → calls main()
    ↓
game.py → SpaceDefenderGame()
    ↓
    ├─ handle_events() → processes input
    ├─ update() → updates entities from entities.py
    │   ├─ Player.update(keys)
    │   ├─ Bullet.update()
    │   ├─ Asteroid.update()
    │   └─ EnemyShip.update()
    │
    ├─ _check_collision() → physics
    ├─ draw() → renders using entities.py.draw()
    └─ Uses constants.py for all config values
    ↓
OUTPUT (Display)
```

## How to Extend

### Add a New Enemy Type
1. Create class in `entities.py` inheriting from `pygame.sprite.Sprite`
2. Implement `update()` and `draw()`  methods
3. Add spawn logic to `game.py`'s `spawn_enemies()`
4. Add scoring to `game.py`'s collision detection

### Change Game Difficulty
1. Open `constants.py`
2. Adjust: `ENEMY_BASE_SPEED`, `ENEMY_SPAWN_RATE`, `WAVE_SIZE`, `TOTAL_WAVES`
3. Run the game - new settings active immediately

### Add a Powerup System
1. Add `Powerup` class to `entities.py`
2. Add spawn logic to `game.py`
3. Handle collision in `game.py`'s update loop
4. Add powerup effects in relevant entity classes

## Code Quality Metrics

| Metric | Value |
|--------|-------|
| Total Lines | ~850 |
| Average File Size | ~170 lines |
| Longest File | game.py (512 lines) |
| Documentation | Full docstrings on all classes/methods |
| Type Hints | Used throughout |
| Code Modularity | High (5 focused modules) |

## Dependencies

- **pygame** (v2.0.0+): Cross-platform game library
  - License: LGPL
  - Used for: Graphics, input, timing

## Running the Game

```bash
# From the module05 directory
python space_defender.py
```

All imports are automatic - no need to run individual modules.

## Future Enhancement Ideas

### Quick Wins (easy to add with current structure)
- Sound effects (add to game.py's update methods)
- Particle effects (new Particle class in entities.py)
- Score persistence (add save_score() to game.py)
- Difficulty levels (multiply constants dynamically)

### Larger Features (would require new modules)
- Networking (new multiplayer.py module)
- Settings menu (new ui.py module)
- Physics engine (new physics.py module)
- AI system (new ai.py module)

## Development Best Practices Applied

✓ Single Responsibility Principle (SRP)  
✓ Don't Repeat Yourself (DRY)  
✓ Separation of Concerns  
✓ Clear naming conventions  
✓ Comprehensive documentation  
✓ Type hints for clarity  
✓ Consistent code style (PEP 8)  
✓ Modular imports (no circular dependencies)  

---

**Last Updated:** March 7, 2026
