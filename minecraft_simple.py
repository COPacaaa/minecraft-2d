"""
2D Minecraft - Simplified Version (No pygame required)
Uses tkinter which is built-in to Python
"""

import tkinter as tk
from tkinter import Canvas
import random
from enum import Enum

class BlockType(Enum):
    """Типы блоков"""
    AIR = 0
    STONE = 1
    DIRT = 2
    GRASS = 3
    WOOD = 4
    SAND = 5

BLOCK_COLORS = {
    BlockType.AIR: "#87CEEB",      # Небо
    BlockType.STONE: "#808080",    # Камень
    BlockType.DIRT: "#8B4513",     # Грязь
    BlockType.GRASS: "#228B22",    # Трава
    BlockType.WOOD: "#654321",     # Дерево
    BlockType.SAND: "#EED6B1",     # Песок
}

class MinecraftGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 2D Minecraft")
        self.root.geometry("1200x700")
        
        # Размеры блоков
        self.block_size = 32
        self.screen_width = 1200
        self.screen_height = 700
        
        # Создаём канвас
        self.canvas = Canvas(root, bg="#87CEEB", width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Мир
        self.world_width = 100
        self.world_height = 50
        self.blocks = [[BlockType.AIR for _ in range(self.world_width)] for _ in range(self.world_height)]
        
        # Генерируем мир
        self.generate_world()
        
        # Игрок
        self.player_x = 50
        self.player_y = 20
        self.player_width = 16
        self.player_height = 32
        self.player_velocity_y = 0
        self.player_velocity_x = 0
        self.is_jumping = False
        
        # Инвентарь
        self.inventory = {
            BlockType.STONE: 64,
            BlockType.DIRT: 64,
            BlockType.WOOD: 32,
            BlockType.SAND: 32,
        }
        self.selected_block = BlockType.DIRT
        
        # Камера
        self.camera_x = 0
        self.camera_y = 0
        
        # Клавиши
        self.keys = {}
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        
        # Игровой цикл
        self.running = True
        self.game_loop()
    
    def generate_world(self):
        """Генерирует мир"""
        ground_level = self.world_height // 2
        
        for y in range(self.world_height):
            for x in range(self.world_width):
                if y >= ground_level:
                    if y == self.world_height - 1:
                        self.blocks[y][x] = BlockType.STONE
                    elif y > ground_level + 10:
                        if random.random() < 0.3:
                            self.blocks[y][x] = BlockType.STONE
                    elif y == ground_level:
                        self.blocks[y][x] = BlockType.GRASS
                    elif y > ground_level - 3:
                        self.blocks[y][x] = BlockType.DIRT
                    else:
                        self.blocks[y][x] = BlockType.STONE
        
        # Деревья
        for _ in range(20):
            x = random.randint(5, self.world_width - 5)
            y = ground_level - 1
            
            for dy in range(4):
                if y - dy >= 0:
                    self.blocks[y - dy][x] = BlockType.WOOD
    
    def key_press(self, event):
        """Нажатие клавиши"""
        self.keys[event.keysym] = True
        
        if event.keysym == "space" and not self.is_jumping:
            self.player_velocity_y = -15
            self.is_jumping = True
        
        if event.keysym == "Escape":
            self.running = False
            self.root.quit()
    
    def key_release(self, event):
        """Отпускание клавиши"""
        self.keys[event.keysym] = False
    
    def on_click(self, event):
        """ЛКМ - ломаем блок"""
        block_x = (event.x + int(self.camera_x)) // self.block_size
        block_y = (event.y + int(self.camera_y)) // self.block_size
        
        if 0 <= block_x < self.world_width and 0 <= block_y < self.world_height:
            self.blocks[block_y][block_x] = BlockType.AIR
    
    def on_right_click(self, event):
        """ПКМ - строим блок"""
        block_x = (event.x + int(self.camera_x)) // self.block_size
        block_y = (event.y + int(self.camera_y)) // self.block_size
        
        if 0 <= block_x < self.world_width and 0 <= block_y < self.world_height:
            if self.inventory[self.selected_block] > 0:
                self.blocks[block_y][block_x] = self.selected_block
                self.inventory[self.selected_block] -= 1
    
    def update(self):
        """Обновление логики"""
        # Движение
        self.player_velocity_x = 0
        if self.keys.get("a"):
            self.player_velocity_x = -5
        if self.keys.get("d"):
            self.player_velocity_x = 5
        
        # Выбор блока
        if self.keys.get("1"):
            self.selected_block = BlockType.DIRT
        if self.keys.get("2"):
            self.selected_block = BlockType.STONE
        if self.keys.get("3"):
            self.selected_block = BlockType.WOOD
        
        # Гравитация
        self.player_velocity_y += 0.6
        if self.player_velocity_y > 20:
            self.player_velocity_y = 20
        
        # Новые позиции
        new_x = self.player_x + self.player_velocity_x
        new_y = self.player_y + self.player_velocity_y
        
        # Коллизии
        block_x_min = int(new_x) // self.block_size
        block_x_max = int(new_x + self.player_width) // self.block_size
        block_y_min = int(new_y) // self.block_size
        block_y_max = int(new_y + self.player_height) // self.block_size
        
        collision = False
        for by in range(max(0, block_y_min), min(self.world_height, block_y_max + 1)):
            for bx in range(max(0, block_x_min), min(self.world_width, block_x_max + 1)):
                if self.blocks[by][bx] != BlockType.AIR:
                    collision = True
                    break
        
        if not collision:
            self.player_x = new_x
            self.player_y = new_y
            self.is_jumping = False
        else:
            if self.player_velocity_y > 0:
                self.player_y = (block_y_min) * self.block_size - self.player_height
                self.player_velocity_y = 0
                self.is_jumping = False
        
        # Камера
        self.camera_x = self.player_x - self.screen_width // 4
        self.camera_y = self.player_y - self.screen_height // 3
    
    def draw(self):
        """Рисование"""
        self.canvas.delete("all")
        
        # Рисуем блоки
        start_x = max(0, int(self.camera_x) // self.block_size)
        start_y = max(0, int(self.camera_y) // self.block_size)
        end_x = min(self.world_width, (int(self.camera_x) + self.screen_width) // self.block_size + 1)
        end_y = min(self.world_height, (int(self.camera_y) + self.screen_height) // self.block_size + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                block = self.blocks[y][x]
                color = BLOCK_COLORS[block]
                
                screen_x = x * self.block_size - int(self.camera_x)
                screen_y = y * self.block_size - int(self.camera_y)
                
                self.canvas.create_rectangle(
                    screen_x, screen_y,
                    screen_x + self.block_size, screen_y + self.block_size,
                    fill=color, outline="black"
                )
        
        # Рисуем игрока
        player_screen_x = self.player_x - int(self.camera_x)
        player_screen_y = self.player_y - int(self.camera_y)
        self.canvas.create_rectangle(
            player_screen_x, player_screen_y,
            player_screen_x + self.player_width, player_screen_y + self.player_height,
            fill="red", outline="darkred"
        )
        
        # HUD
        self.canvas.create_text(
            10, 10,
            text=f"❤️  20/20 | 🍖 20/20",
            fill="white", font=("Arial", 14), anchor="nw"
        )
        
        inv_text = f"Инвентарь - 1:Грязь({self.inventory[BlockType.DIRT]}) 2:Камень({self.inventory[BlockType.STONE]}) 3:Дерево({self.inventory[BlockType.WOOD]})"
        self.canvas.create_text(
            10, self.screen_height - 30,
            text=inv_text,
            fill="white", font=("Arial", 12), anchor="nw"
        )
        
        controls = "A/D-движение | SPACE-прыжок | ЛКМ-ломать | ПКМ-строить | 1/2/3-выбор блока"
        self.canvas.create_text(
            10, self.screen_height - 10,
            text=controls,
            fill="white", font=("Arial", 10), anchor="nw"
        )
    
    def game_loop(self):
        """Главный цикл игры"""
        if self.running:
            self.update()
            self.draw()
            self.root.after(30, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = MinecraftGame(root)
    root.mainloop()
