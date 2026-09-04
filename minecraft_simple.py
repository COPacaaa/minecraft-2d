"""
2D Minecraft - Улучшенная версия с модельками и лучшим управлением
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
    LEAVES = 6
    WATER = 7
    DIAMOND = 8

# Цвета блоков
BLOCK_COLORS = {
    BlockType.AIR: "#87CEEB",
    BlockType.STONE: "#808080",
    BlockType.DIRT: "#8B4513",
    BlockType.GRASS: "#228B22",
    BlockType.WOOD: "#654321",
    BlockType.SAND: "#EED6B1",
    BlockType.LEAVES: "#006400",
    BlockType.WATER: "#4169E1",
    BlockType.DIAMOND: "#00CED1",
}

def draw_block(canvas, x, y, size, block_type):
    """Рисует блок с текстурой"""
    color = BLOCK_COLORS[block_type]
    
    # Основной блок
    canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline="black", width=1)
    
    if block_type == BlockType.GRASS:
        # Трава на вершине
        canvas.create_polygon(
            x, y + size//2, x + size//4, y + size//4, x + size//2, y,
            fill="darkgreen", outline="darkgreen"
        )
        canvas.create_polygon(
            x + size//2, y, x + size*3//4, y + size//4, x + size, y + size//2,
            fill="green", outline="green"
        )
    
    elif block_type == BlockType.WOOD:
        # Годичные кольца на дереве
        canvas.create_oval(x + size//4, y + size//4, x + size*3//4, y + size*3//4, 
                          outline="brown", width=2)
        canvas.create_oval(x + size//3, y + size//3, x + size*2//3, y + size*2//3, 
                          outline="saddlebrown", width=1)
    
    elif block_type == BlockType.LEAVES:
        # Листья
        for i in range(3):
            offset_x = (i - 1) * (size // 3)
            canvas.create_oval(x + size//3 + offset_x, y + size//3 - 2, 
                              x + size//3 + offset_x + size//3, y + size*2//3,
                              fill="darkgreen", outline="green")
    
    elif block_type == BlockType.SAND:
        # Песок с точками
        for i in range(4):
            px = x + (i % 2) * size//2 + size//4
            py = y + (i // 2) * size//2 + size//4
            canvas.create_oval(px - 2, py - 2, px + 2, py + 2, fill="tan", outline="tan")
    
    elif block_type == BlockType.STONE:
        # Камень с трещинами
        canvas.create_line(x, y + size//3, x + size, y + size//3, fill="gray", width=1)
        canvas.create_line(x + size//2, y, x + size//2, y + size, fill="gray", width=1)
    
    elif block_type == BlockType.WATER:
        # Волны на воде
        canvas.create_arc(x, y, x + size, y + size, start=0, extent=180, 
                         outline="blue", width=2)
    
    elif block_type == BlockType.DIAMOND:
        # Алмаз - ромб
        diamond_offset = size // 4
        canvas.create_polygon(
            x + size//2, y + diamond_offset,
            x + size - diamond_offset, y + size//2,
            x + size//2, y + size - diamond_offset,
            x + diamond_offset, y + size//2,
            fill="cyan", outline="darkturquoise", width=2
        )

def draw_player(canvas, x, y, width, height, color="red"):
    """Рисует игрока с лицом"""
    # Голова
    head_size = height // 3
    canvas.create_rectangle(x + width//4, y, x + width*3//4, y + head_size, 
                           fill=color, outline="darkred", width=2)
    
    # Глаза
    eye_offset = width // 6
    canvas.create_oval(x + eye_offset - 2, y + head_size//4 - 2, 
                      x + eye_offset + 2, y + head_size//4 + 2, 
                      fill="white", outline="black")
    canvas.create_oval(x + width - eye_offset - 2, y + head_size//4 - 2, 
                      x + width - eye_offset + 2, y + head_size//4 + 2, 
                      fill="white", outline="black")
    
    # Зрачки
    canvas.create_oval(x + eye_offset - 1, y + head_size//4 - 1, 
                      x + eye_offset + 1, y + head_size//4 + 1, fill="black")
    canvas.create_oval(x + width - eye_offset - 1, y + head_size//4 - 1, 
                      x + width - eye_offset + 1, y + head_size//4 + 1, fill="black")
    
    # Рот
    canvas.create_arc(x + width//4 + 2, y + head_size//2, x + width*3//4 - 2, 
                     y + head_size*2//3, start=0, extent=180, 
                     outline="black", width=1)
    
    # Туловище
    canvas.create_rectangle(x + width//6, y + head_size, x + width*5//6, y + height*2//3, 
                           fill=color, outline="darkred", width=2)
    
    # Руки
    canvas.create_rectangle(x - 2, y + head_size + 2, x + width//6, y + height//2, 
                           fill=color, outline="darkred", width=1)
    canvas.create_rectangle(x + width*5//6, y + head_size + 2, x + width + 2, y + height//2, 
                           fill=color, outline="darkred", width=1)
    
    # Ноги
    canvas.create_rectangle(x + width//4, y + height*2//3, x + width//2 - 1, y + height, 
                           fill=color, outline="darkred", width=2)
    canvas.create_rectangle(x + width//2 + 1, y + height*2//3, x + width*3//4, y + height, 
                           fill=color, outline="darkred", width=2)

class MinecraftGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 2D Minecraft - УЛУЧШЕННАЯ")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        # Размеры блоков
        self.block_size = 32
        self.screen_width = 1200
        self.screen_height = 700
        
        # Создаём канвас
        self.canvas = Canvas(root, bg="#87CEEB", width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Мир
        self.world_width = 100
        self.world_height = 50
        self.blocks = [[BlockType.AIR for _ in range(self.world_width)] for _ in range(self.world_height)]
        
        # Генерируем мир
        self.generate_world()
        
        # Игрок
        self.player_x = 50 * self.block_size
        self.player_y = 15 * self.block_size
        self.player_width = 16
        self.player_height = 32
        self.player_velocity_y = 0
        self.player_velocity_x = 0
        self.is_jumping = False
        self.is_on_ground = False
        self.move_left = False
        self.move_right = False
        
        # Инвентарь
        self.inventory = {
            BlockType.STONE: 64,
            BlockType.DIRT: 64,
            BlockType.WOOD: 32,
            BlockType.SAND: 32,
            BlockType.LEAVES: 32,
            BlockType.DIAMOND: 5,
        }
        self.selected_block = BlockType.DIRT
        self.selected_index = 0
        
        # Камера
        self.camera_x = 0
        self.camera_y = 0
        
        # Клавиши
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        
        # Игровой цикл
        self.running = True
        self.game_loop()
    
    def generate_world(self):
        """Генерирует мир с красивым ландшафтом"""
        ground_level = self.world_height // 2
        
        for y in range(self.world_height):
            for x in range(self.world_width):
                if y >= ground_level:
                    if y == self.world_height - 1:
                        self.blocks[y][x] = BlockType.STONE
                    elif y > ground_level + 15:
                        if random.random() < 0.5:
                            self.blocks[y][x] = BlockType.STONE
                        else:
                            self.blocks[y][x] = BlockType.DIRT
                    elif y == ground_level:
                        self.blocks[y][x] = BlockType.GRASS
                    elif y > ground_level - 3:
                        self.blocks[y][x] = BlockType.DIRT
                    else:
                        self.blocks[y][x] = BlockType.STONE
        
        # Деревья
        for _ in range(15):
            x = random.randint(5, self.world_width - 5)
            y = ground_level - 1
            
            # Ствол
            for dy in range(4):
                if y - dy >= 0:
                    self.blocks[y - dy][x] = BlockType.WOOD
            
            # Листья
            for lx in range(x - 2, x + 3):
                for ly in range(y - 4, y - 1):
                    if 0 <= lx < self.world_width and 0 <= ly < self.world_height:
                        if random.random() > 0.3:
                            self.blocks[ly][lx] = BlockType.LEAVES
        
        # Вода
        water_level = ground_level + 3
        for x in range(10, 30):
            self.blocks[water_level][x] = BlockType.WATER
        
        # Алмазы глубоко под землёй
        for _ in range(5):
            dx = random.randint(10, self.world_width - 10)
            dy = random.randint(self.world_height - 10, self.world_height - 5)
            if 0 <= dx < self.world_width and 0 <= dy < self.world_height:
                self.blocks[dy][dx] = BlockType.DIAMOND
    
    def key_press(self, event):
        """Нажатие клавиши"""
        key = event.keysym.lower()
        
        if key == 'a':
            self.move_left = True
        elif key == 'd':
            self.move_right = True
        elif key == 'space' and self.is_on_ground:
            self.player_velocity_y = -12
            self.is_jumping = True
            self.is_on_ground = False
        elif key == 'escape':
            self.running = False
            self.root.quit()
        
        # Выбор блока
        if key == '1':
            self.selected_block = BlockType.DIRT
            self.selected_index = 0
        elif key == '2':
            self.selected_block = BlockType.STONE
            self.selected_index = 1
        elif key == '3':
            self.selected_block = BlockType.WOOD
            self.selected_index = 2
        elif key == '4':
            self.selected_block = BlockType.SAND
            self.selected_index = 3
        elif key == '5':
            self.selected_block = BlockType.LEAVES
            self.selected_index = 4
        elif key == '6':
            self.selected_block = BlockType.DIAMOND
            self.selected_index = 5
    
    def key_release(self, event):
        """Отпускание клавиши"""
        key = event.keysym.lower()
        
        if key == 'a':
            self.move_left = False
        elif key == 'd':
            self.move_right = False
    
    def on_click(self, event):
        """ЛКМ - ломаем блок"""
        block_x = (event.x + int(self.camera_x)) // self.block_size
        block_y = (event.y + int(self.camera_y)) // self.block_size
        
        if 0 <= block_x < self.world_width and 0 <= block_y < self.world_height:
            block = self.blocks[block_y][block_x]
            self.blocks[block_y][block_x] = BlockType.AIR
            
            # Добавляем в инвентарь
            if block in self.inventory:
                self.inventory[block] += 1
    
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
        if self.move_left:
            self.player_velocity_x = -5
        if self.move_right:
            self.player_velocity_x = 5
        
        # Гравитация
        self.player_velocity_y += 0.6
        if self.player_velocity_y > 20:
            self.player_velocity_y = 20
        
        # Новые позиции
        new_x = self.player_x + self.player_velocity_x
        new_y = self.player_y + self.player_velocity_y
        
        # Проверка коллизий по X
        block_x_min = int(new_x) // self.block_size
        block_x_max = int(new_x + self.player_width) // self.block_size
        block_y_min = int(self.player_y) // self.block_size
        block_y_max = int(self.player_y + self.player_height) // self.block_size
        
        collision_x = False
        for by in range(max(0, block_y_min), min(self.world_height, block_y_max + 1)):
            for bx in range(max(0, block_x_min), min(self.world_width, block_x_max + 1)):
                if self.blocks[by][bx] != BlockType.AIR:
                    collision_x = True
                    break
        
        if not collision_x:
            self.player_x = new_x
        
        # Проверка коллизий по Y
        block_x_min = int(self.player_x) // self.block_size
        block_x_max = int(self.player_x + self.player_width) // self.block_size
        block_y_min = int(new_y) // self.block_size
        block_y_max = int(new_y + self.player_height) // self.block_size
        
        collision_y = False
        self.is_on_ground = False
        
        for by in range(max(0, block_y_min), min(self.world_height, block_y_max + 1)):
            for bx in range(max(0, block_x_min), min(self.world_width, block_x_max + 1)):
                if self.blocks[by][bx] != BlockType.AIR:
                    collision_y = True
                    if self.player_velocity_y > 0:
                        self.is_on_ground = True
                    break
        
        if not collision_y:
            self.player_y = new_y
        else:
            if self.player_velocity_y > 0:
                self.player_y = (block_y_min) * self.block_size - self.player_height
                self.player_velocity_y = 0
            else:
                self.player_y = (block_y_max + 1) * self.block_size
                self.player_velocity_y = 0
        
        # Камера следует за игроком
        self.camera_x = self.player_x - self.screen_width // 4
        self.camera_y = self.player_y - self.screen_height // 3
        
        # Границы камеры
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_y < 0:
            self.camera_y = 0
    
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
                
                screen_x = x * self.block_size - int(self.camera_x)
                screen_y = y * self.block_size - int(self.camera_y)
                
                draw_block(self.canvas, screen_x, screen_y, self.block_size, block)
        
        # Рисуем игрока
        player_screen_x = self.player_x - int(self.camera_x)
        player_screen_y = self.player_y - int(self.camera_y)
        draw_player(self.canvas, player_screen_x, player_screen_y, self.player_width, self.player_height, "red")
        
        # HUD - Здоровье и голод
        self.canvas.create_text(
            10, 10,
            text="❤️ 20/20  | 🍖 20/20",
            fill="white", font=("Arial", 14, "bold"), anchor="nw",
            bg="black"
        )
        
        # Инвентарь
        inv_text = f"1:Грязь({self.inventory[BlockType.DIRT]}) 2:Камень({self.inventory[BlockType.STONE]}) 3:Дерево({self.inventory[BlockType.WOOD]}) 4:Песок({self.inventory[BlockType.SAND]}) 5:Листья({self.inventory[BlockType.LEAVES]}) 6:♦({self.inventory[BlockType.DIAMOND]})"
        self.canvas.create_text(
            10, self.screen_height - 50,
            text=inv_text,
            fill="white", font=("Arial", 11), anchor="nw",
            bg="black"
        )
        
        # Выбранный блок
        block_name = {
            BlockType.DIRT: "Грязь",
            BlockType.STONE: "Камень",
            BlockType.WOOD: "Дерево",
            BlockType.SAND: "Песок",
            BlockType.LEAVES: "Листья",
            BlockType.DIAMOND: "Алмаз",
        }
        self.canvas.create_text(
            10, self.screen_height - 30,
            text=f"✓ Выбран: {block_name[self.selected_block]}",
            fill="yellow", font=("Arial", 12, "bold"), anchor="nw",
            bg="black"
        )
        
        # Управление
        controls = "A/D-ходить | SPACE-прыгать | ЛКМ-ломать | ПКМ-строить | 1-6-выбор блока | ESC-выход"
        self.canvas.create_text(
            10, self.screen_height - 10,
            text=controls,
            fill="lime", font=("Arial", 10), anchor="nw",
            bg="black"
        )
    
    def game_loop(self):
        """Главный цикл игры"""
        if self.running:
            self.update()
            self.draw()
            self.root.after(20, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = MinecraftGame(root)
    root.mainloop()
