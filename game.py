import pygame
import random
from player import Player
from world import World
from ui import UI

class Game:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        
        # Create world and player
        self.world = World(width, height, tile_size)
        self.player = Player(5, 5, tile_size)
        
        # UI
        self.ui = UI(width, height)
        
        # Game state
        self.selected_block = 1  # 1 = dirt, 2 = grass, 3 = stone, etc.
        self.game_time = 0
        self.paused = False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
            elif event.key == pygame.K_1:
                self.selected_block = 1  # Dirt
            elif event.key == pygame.K_2:
                self.selected_block = 2  # Grass
            elif event.key == pygame.K_3:
                self.selected_block = 3  # Stone
            elif event.key == pygame.K_4:
                self.selected_block = 0  # Air (delete)
            elif event.key == pygame.K_SPACE:
                self.player.jump()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:  # Left click - place block
                self.place_block(mouse_pos)
            elif event.button == 3:  # Right click - break block
                self.break_block(mouse_pos)
    
    def place_block(self, mouse_pos):
        # Convert mouse position to world coordinates
        camera_x = self.player.x - self.width // (2 * self.tile_size)
        camera_y = self.player.y - self.height // (2 * self.tile_size)
        
        world_x = (mouse_pos[0] // self.tile_size) + camera_x
        world_y = (mouse_pos[1] // self.tile_size) + camera_y
        
        if self.selected_block > 0:
            self.world.set_block(world_x, world_y, self.selected_block)
    
    def break_block(self, mouse_pos):
        # Convert mouse position to world coordinates
        camera_x = self.player.x - self.width // (2 * self.tile_size)
        camera_y = self.player.y - self.height // (2 * self.tile_size)
        
        world_x = (mouse_pos[0] // self.tile_size) + camera_x
        world_y = (mouse_pos[1] // self.tile_size) + camera_y
        
        self.world.set_block(world_x, world_y, 0)  # Air
    
    def update(self):
        if not self.paused:
            # Update player
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)
            self.player.update(self.world)
            
            # Update world
            self.world.update()
            self.game_time += 1
    
    def draw(self, screen):
        # Draw world
        self.world.draw(screen, self.player.x, self.player.y, self.width, self.height)
        
        # Draw player
        self.player.draw(screen, self.width, self.height)
        
        # Draw UI
        self.ui.draw(screen, self.selected_block, self.paused, self.game_time)
