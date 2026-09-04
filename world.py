import pygame
import random
import numpy as np

class World:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        # World dimensions (in tiles)
        self.world_width = 1000
        self.world_height = 200
        
        # Block types: 0=air, 1=dirt, 2=grass, 3=stone, 4=sand, 5=water
        self.blocks = np.zeros((self.world_width, self.world_height), dtype=int)
        
        # Colors for blocks
        self.block_colors = {
            0: (135, 206, 235),  # Air (sky blue)
            1: (139, 69, 19),    # Dirt
            2: (34, 139, 34),    # Grass
            3: (128, 128, 128),  # Stone
            4: (238, 213, 183),  # Sand
            5: (30, 144, 255),   # Water
        }
        
        self.generate_world()
    
    def generate_world(self):
        """Generate terrain using simple noise"""
        # Create ground
        for x in range(self.world_width):
            # Calculate height variation
            height = 100 + int(20 * np.sin(x / 50)) + random.randint(-5, 5)
            
            for y in range(height, self.world_height):
                if y == height:
                    self.blocks[x, y] = 2  # Grass on top
                elif y < height + 3:
                    self.blocks[x, y] = 1  # Dirt
                else:
                    self.blocks[x, y] = 3  # Stone
            
            # Add some features
            if random.random() < 0.1 and height > 0:
                # Place trees
                for i in range(random.randint(3, 6)):
                    if height - i - 1 > 0:
                        self.blocks[x, height - i - 1] = 4  # Wood (using sand as placeholder)
    
    def get_block(self, x, y):
        """Get block at position"""
        if 0 <= x < self.world_width and 0 <= y < self.world_height:
            return self.blocks[x, y]
        return 0
    
    def set_block(self, x, y, block_type):
        """Set block at position"""
        if 0 <= x < self.world_width and 0 <= y < self.world_height:
            self.blocks[x, y] = block_type
    
    def update(self):
        """Update world state (water flow, etc.)"""
        pass
    
    def draw(self, screen, camera_x, camera_y, screen_width, screen_height):
        """Draw visible blocks"""
        # Calculate visible range
        start_x = max(0, int(camera_x) - screen_width // (2 * self.tile_size))
        end_x = min(self.world_width, int(camera_x) + screen_width // (2 * self.tile_size) + 1)
        
        start_y = max(0, int(camera_y) - screen_height // (2 * self.tile_size))
        end_y = min(self.world_height, int(camera_y) + screen_height // (2 * self.tile_size) + 1)
        
        # Draw blocks
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                block = self.blocks[x, y]
                if block > 0:
                    # Calculate screen position
                    screen_x = (x - camera_x) * self.tile_size + screen_width // 2
                    screen_y = (y - camera_y) * self.tile_size + screen_height // 2
                    
                    # Draw block
                    color = self.block_colors.get(block, (255, 255, 255))
                    pygame.draw.rect(screen, color,
                                   (screen_x, screen_y, self.tile_size, self.tile_size))
                    
                    # Draw border
                    pygame.draw.rect(screen, (0, 0, 0),
                                   (screen_x, screen_y, self.tile_size, self.tile_size), 1)
