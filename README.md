# 2D Minecraft Game

A 2D sandbox game inspired by Minecraft, built with Python and Pygame.

## Features

✨ **Core Gameplay**
- 2D world with procedurally generated terrain
- Block placing and breaking
- Player movement and jumping with physics
- Collision detection
- Multiple block types (Dirt, Grass, Stone, Sand)

🎮 **Controls**
- **WASD or Arrow Keys**: Move left/right
- **Space**: Jump
- **1-4**: Select block type
- **Left Click**: Place block
- **Right Click**: Break block
- **ESC**: Pause game

## Installation

### Requirements
- Python 3.8+
- Pygame
- NumPy

### Setup

1. Clone the repository:
```bash
git clone https://github.com/COPacaaa/minecraft-2d.git
cd minecraft-2d
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Project Structure

```
minecraft-2d/
├── main.py           # Entry point and game loop
├── game.py           # Main game logic and state management
├── player.py         # Player class with physics
├── world.py          # World generation and block management
├── ui.py             # UI and HUD rendering
└── requirements.txt  # Python dependencies
```

## Block Types

| Block | ID | Color |
|-------|----|---------|
| Air | 0 | Transparent |
| Dirt | 1 | Brown |
| Grass | 2 | Green |
| Stone | 3 | Gray |
| Sand | 4 | Tan |
| Water | 5 | Blue |

## Future Features

- [ ] More block types and materials
- [ ] Inventory system
- [ ] Crafting system
- [ ] Mining speed for different tools
- [ ] Water physics and swimming
- [ ] Day/night cycle with lighting
- [ ] Mob system
- [ ] Sound effects and music
- [ ] Save/load world system
- [ ] Improved terrain generation

## Tips

1. **Explore**: The world extends horizontally, try moving in different directions
2. **Build**: Use left-click to place blocks and create structures
3. **Mine**: Use right-click to break blocks and gather materials
4. **Jump**: Use space to reach higher places and avoid falling

## License

MIT License - feel free to modify and distribute

## Author

COPacaaa
