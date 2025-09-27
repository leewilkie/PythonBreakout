# Breakout Game

## Overview
This is a classic Breakout game implemented in Python using Pygame. It's a complete arcade-style game where players control a paddle to bounce a ball and break colored bricks. The game features multiple powerups, lives system, scoring, and smooth gameplay.

## Recent Changes
- **2025-09-27**: Successfully imported GitHub project and configured for Replit environment
- Installed Python 3.11 and pygame 2.6.1 dependencies
- Created requirements.txt for dependency management
- Configured workflow to run the game
- Project tested and confirmed working

## Project Architecture

### Core Game Files
- `breakout.py` - Main game file containing the game loop, rendering, and core logic
- `ball.py` - Ball class with physics and collision properties
- `brick.py` - Brick class with hit detection and destruction logic
- `bricktype.py` - Brick type definitions for different brick properties
- `powerup.py` - Powerup system with various effects (laser, multiball, wide bat, power ball)
- `bullet.py` - Bullet mechanics for laser powerup
- `sprite.py` - Basic sprite rectangle class
- `sprites.py` - Sprite coordinate definitions for the sprite sheet
- `level.py` - Level management (currently basic implementation)

### Assets
- `sprites.png` - Game sprite sheet containing all visual assets
- `level1.json` - Level configuration file

### Game Features
- Classic breakout gameplay with paddle and ball physics
- Multiple powerup types:
  - Laser: Shoot bullets to destroy bricks
  - Multiball: Split ball into multiple balls
  - Wide Bat: Increase paddle width
  - Power Ball: Ball destroys bricks without bouncing
- Lives system (3 lives)
- Score tracking
- Pause functionality (spacebar)
- Mouse and keyboard controls
- Shadow effects for visual depth
- Background tiling system

### Technical Details
- **Language**: Python 3.11
- **Framework**: Pygame 2.6.1
- **Architecture**: Object-oriented design with separate classes for game entities
- **Resolution**: 672x768 pixels (224x256 * 3 scale factor)
- **FPS**: 60 frames per second

### Dependencies
- pygame==2.6.1

### How to Run
The game is configured to run automatically via the Replit workflow. The main entry point is `breakout.py`.

### Controls
- Mouse movement: Move paddle left/right
- Left mouse click: Fire laser bullets (when laser powerup is active)
- Left/Right arrow keys: Alternative paddle movement
- Spacebar: Pause/unpause game

## Development Notes
- Game uses a component-based architecture with separate classes for each game entity
- Sprite system uses coordinate-based indexing into a sprite sheet
- Physics system handles ball bouncing, paddle interaction, and collision detection
- Powerup system is extensible for adding new powerup types
- Game state is managed through global variables in the main game loop