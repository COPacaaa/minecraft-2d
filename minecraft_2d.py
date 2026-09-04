"""
2D Minecraft - основной движок игры
"""

import pygame
import random
import json
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple

pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BLOCK_SIZE = 32
FPS = 60

class BlockType(Enum):
    """Типы блоков"""
    AIR = 0
    STONE = 1
    DIRT = 2
    GRASS = 3
    OAK_LOG = 4
    OAK_LEAVES = 5
    SAND = 6
    WATER = 7
    COAL_ORE = 8
    IRON_ORE = 9
    DIAMOND_ORE = 10
    BEDROCK = 11

BLOCK_COLORS = {
    BlockType.AIR: (135, 206, 235),  # Небо
    BlockType.STONE: (128, 128, 128),  # Камень
    BlockType.DIRT: (139, 69, 19),  # Грязь
    BlockType.GRASS: (34, 139, 34),  # Трава
    BlockType.OAK_LOG: (101, 67, 33),  # Бревно
    BlockType.OAK_LEAVES: (34, 180, 34),  # Листья
    BlockType.SAND: (238, 214, 175),  # Песок
    BlockType.WATER: (30, 144, 255),  # Вода
    BlockType.COAL_ORE: (32, 32, 32),  # Уголь
    BlockType.IRON_ORE: (192, 192, 192),  # Железо
    BlockType.DIAMOND_ORE: (100, 200, 255),  # Алмаз
    BlockType.BEDROCK: (16, 16, 16),  # Коренная порода
}

@dataclass
class Player:
    """Игрок"""
    x: float
    y: float
    width: int = 16
    height: int = 32
    velocity_y: float = 0
    velocity_x: float = 0
    is_jumping: bool = False
    health: int = 20
    hunger: int = 20
    inventory: dict = None
    selected_block: BlockType = BlockType.DIRT
    
    def __post_init__(self):
        if self.inventory is None:
            self.inventory = {
                BlockType.STONE: 64,
                BlockType.DIRT: 64,
                BlockType.GRASS: 32,
                BlockType.OAK_LOG: 32,
                BlockType.SAND: 32,
            }

class World:
    """Мир игры"""
    
    def __init__(self, width: int = 200, height: int = 100):
        self.width = width
        self.height = height
        self.blocks = [[BlockType.AIR for _ in range(width)] for _ in range(height)]
        self.generate_world()
    
    def generate_world(self):
        """Генерирует мир"""
        # Создаём слои земли
        ground_level = self.height // 2
        
        for y in range(self.height):
            for x in range(self.width):
                if y >= ground_level:
                    # Коренная порода внизу
                    if y == self.height - 1:
                        self.blocks[y][x] = BlockType.BEDROCK
                    # Камень глубоко
                    elif y > ground_level + 20:
                        if random.random() < 0.1:
                            self.blocks[y][x] = BlockType.COAL_ORE
                        elif random.random() < 0.05:
                            self.blocks[y][x] = BlockType.IRON_ORE
                        elif random.random() < 0.02:
                            self.blocks[y][x] = BlockType.DIAMOND_ORE
                        else:
                            self.blocks[y][x] = BlockType.STONE
                    # Грязь и трава
                    elif y == ground_level:
                        self.blocks[y][x] = BlockType.GRASS
                    elif y > ground_level - 4:
                        self.blocks[y][x] = BlockType.DIRT
                    else:
                        self.blocks[y][x] = BlockType.STONE
        
        # Генерируем деревья
        self._generate_trees(ground_level)
        
        # Генерируем озёра
        self._generate_lakes(ground_level)
    
    def _generate_trees(self, ground_level: int):
        """Генерирует деревья"""
        for _ in range(30):
            x = random.randint(5, self.width - 5)
            y = ground_level - 1
            
            # Бревно
            for dy in range(5):
                if y - dy >= 0:
                    self.blocks[y - dy][x] = BlockType.OAK_LOG
            
            # Листья
            for dx in range(-2, 3):
                for dy in range(-3, 2):
                    nx, ny = x + dx, y - 5 + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.blocks[ny][nx] == BlockType.AIR:
                            self.blocks[ny][nx] = BlockType.OAK_LEAVES
    
    def _generate_lakes(self, ground_level: int):
        """Генерирует озёра"""
        for _ in range(5):
            x = random.randint(10, self.width - 10)
            y = ground_level
            
            for dx in range(-5, 6):
                for dy in range(-3, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if self.blocks[ny][nx] in [BlockType.DIRT, BlockType.GRASS]:
                            self.blocks[ny][nx] = BlockType.WATER
    
    def get_block(self, x: int, y: int) -> BlockType:
        """Получает блок по координатам"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.blocks[y][x]
        return BlockType.BEDROCK
    
    def set_block(self, x: int, y: int, block_type: BlockType):
        """Устанавливает блок"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.blocks[y][x] = block_type
    
    def break_block(self, x: int, y: int):
        """Ломает блок"""
        if self.get_block(x, y) != BlockType.BEDROCK:
            self.set_block(x, y, BlockType.AIR)

class MinecraftGame:
    """Основной класс игры"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 2D Minecraft")
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        
        # Создаём мир и игрока
        self.world = World()
        self.player = Player(x=100, y=100)
        
        # Камера
        self.camera_x = 0
        self.camera_y = 0
        
        # Шрифт
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 48)
        
        # Игровое время
        self.time = 0
        self.day_length = 12000  # Тики
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                
                if event.key == pygame.K_SPACE and not self.player.is_jumping:
                    self.player.velocity_y = -15
                    self.player.is_jumping = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ - ломаем
                    self._break_block()
                elif event.button == 3:  # ПКМ - строим
                    self._place_block()
    
    def _break_block(self):
        """Ломает блок"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        block_x = (mouse_x + self.camera_x) // BLOCK_SIZE
        block_y = (mouse_y + self.camera_y) // BLOCK_SIZE
        self.world.break_block(block_x, block_y)
    
    def _place_block(self):
        """Строит блок"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        block_x = (mouse_x + self.camera_x) // BLOCK_SIZE
        block_y = (mouse_y + self.camera_y) // BLOCK_SIZE
        
        if self.player.inventory[self.player.selected_block] > 0:
            self.world.set_block(block_x, block_y, self.player.selected_block)
            self.player.inventory[self.player.selected_block] -= 1
    
    def update(self):
        """Обновление логики"""
        if self.paused:
            return
        
        self.time += 1
        
        # Управление
        keys = pygame.key.get_pressed()
        
        # Горизонтальное движение
        self.player.velocity_x = 0
        if keys[pygame.K_a]:
            self.player.velocity_x = -5
        if keys[pygame.K_d]:
            self.player.velocity_x = 5
        
        # Применяем гравитацию
        self.player.velocity_y += 0.6
        if self.player.velocity_y > 20:
            self.player.velocity_y = 20
        
        # Новые позиции
        new_x = self.player.x + self.player.velocity_x
        new_y = self.player.y + self.player.velocity_y
        
        # Коллизии
        player_rect = pygame.Rect(new_x, new_y, self.player.width, self.player.height)
        
        # Проверяем столкновения с блоками
        block_x_min = int(new_x) // BLOCK_SIZE
        block_x_max = int(new_x + self.player.width) // BLOCK_SIZE
        block_y_min = int(new_y) // BLOCK_SIZE
        block_y_max = int(new_y + self.player.height) // BLOCK_SIZE
        
        collision = False
        for by in range(block_y_min, block_y_max + 1):
            for bx in range(block_x_min, block_x_max + 1):
                if self.world.get_block(bx, by) != BlockType.AIR:
                    collision = True
                    break
        
        if not collision:
            self.player.x = new_x
            self.player.y = new_y
            self.player.is_jumping = False
        else:
            # Упираемся в блок
            if self.player.velocity_y > 0:
                self.player.y = (block_y_min) * BLOCK_SIZE - self.player.height
                self.player.velocity_y = 0
                self.player.is_jumping = False
            elif self.player.velocity_y < 0:
                self.player.y = (block_y_max + 1) * BLOCK_SIZE
                self.player.velocity_y = 0
        
        # Обновляем камеру
        self.camera_x = self.player.x - SCREEN_WIDTH // 4
        self.camera_y = self.player.y - SCREEN_HEIGHT // 3
    
    def draw(self):
        """Рисование"""
        self.screen.fill((135, 206, 235))  # Небо
        
        # Рисуем блоки
        start_x = max(0, int(self.camera_x) // BLOCK_SIZE)
        start_y = max(0, int(self.camera_y) // BLOCK_SIZE)
        end_x = min(self.world.width, (int(self.camera_x) + SCREEN_WIDTH) // BLOCK_SIZE + 1)
        end_y = min(self.world.height, (int(self.camera_y) + SCREEN_HEIGHT) // BLOCK_SIZE + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                block = self.world.get_block(x, y)
                color = BLOCK_COLORS[block]
                
                screen_x = x * BLOCK_SIZE - int(self.camera_x)
                screen_y = y * BLOCK_SIZE - int(self.camera_y)
                
                pygame.draw.rect(self.screen, color, (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, (0, 0, 0), (screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE), 1)
        
        # Рисуем игрока
        player_screen_x = self.player.x - int(self.camera_x)
        player_screen_y = self.player.y - int(self.camera_y)
        pygame.draw.rect(self.screen, (255, 100, 100), (player_screen_x, player_screen_y, self.player.width, self.player.height))
        
        # HUD
        self._draw_hud()
    
    def _draw_hud(self):
        """Рисует интерфейс"""
        # Здоровье
        health_text = self.font.render(f"❤️  {self.player.health}/20", True, (255, 0, 0))
        self.screen.blit(health_text, (10, 10))
        
        # Голод
        hunger_text = self.font.render(f"🍖 {self.player.hunger}/20", True, (255, 165, 0))
        self.screen.blit(hunger_text, (10, 40))
        
        # Время суток
        day_progress = (self.time % self.day_length) / self.day_length
        time_text = self.font.render(f"🌙 Day {self.time // self.day_length + 1}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 70))
        
        # Инвентарь
        inv_text = self.font.render("Инвентарь (E):", True, (255, 255, 255))
        self.screen.blit(inv_text, (10, SCREEN_HEIGHT - 60))
        
        y_offset = SCREEN_HEIGHT - 30
        for block_type, count in self.player.inventory.items():
            block_text = self.font.render(f"{block_type.name}: {count}", True, (200, 200, 200))
            self.screen.blit(block_text, (10, y_offset))
            y_offset -= 25
        
        # Управление
        if self.paused:
            pause_text = self.font_large.render("ПАУЗА", True, (255, 0, 0))
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
        
        controls = self.font.render("A/D - движение | SPACE - прыжок | ЛКМ - ломать | ПКМ - строить | ESC - пауза", True, (200, 200, 200))
        self.screen.blit(controls, (10, SCREEN_HEIGHT - 90))
    
    def run(self):
        """Запуск игры"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = MinecraftGame()
    game.run()
