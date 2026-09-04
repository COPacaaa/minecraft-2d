import pygame

class Player:
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        
        # Physics
        self.vx = 0
        self.vy = 0
        self.is_jumping = False
        self.on_ground = False
        
        # Constants
        self.SPEED = 0.15
        self.JUMP_FORCE = 0.4
        self.GRAVITY = 0.02
        self.MAX_FALL_SPEED = 0.5
        
        # Size
        self.width = 0.8
        self.height = 1.8
    
    def handle_input(self, keys):
        # Horizontal movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.SPEED
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.SPEED
        else:
            self.vx = 0
    
    def jump(self):
        if self.on_ground:
            self.vy = -self.JUMP_FORCE
            self.is_jumping = True
            self.on_ground = False
    
    def update(self, world):
        # Apply gravity
        self.vy += self.GRAVITY
        if self.vy > self.MAX_FALL_SPEED:
            self.vy = self.MAX_FALL_SPEED
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Collision detection
        self.on_ground = False
        
        # Check collisions with blocks
        for dx in [-self.width/2, self.width/2]:
            for dy in [-self.height/2, self.height/2]:
                check_x = int(self.x + dx)
                check_y = int(self.y + dy)
                
                if world.get_block(check_x, check_y) > 0:
                    # Collision detected
                    if self.vy > 0:  # Falling
                        self.y = check_y - self.height/2 - 0.1
                        self.vy = 0
                        self.on_ground = True
                        self.is_jumping = False
                    elif self.vy < 0:  # Jumping
                        self.y = check_y + 1 + self.height/2 + 0.1
                        self.vy = 0
                    
                    if self.vx > 0:  # Moving right
                        self.x = check_x - self.width/2 - 0.1
                    elif self.vx < 0:  # Moving left
                        self.x = check_x + 1 + self.width/2 + 0.1
        
        # Keep player in world bounds
        if self.x < 0:
            self.x = 0
        if self.y > 100:  # Fall limit
            self.x = 5
            self.y = 5
    
    def draw(self, screen, screen_width, screen_height):
        # Draw player at center of screen
        player_screen_x = screen_width // 2
        player_screen_y = screen_height // 2
        
        # Draw player as a simple rectangle
        pygame.draw.rect(screen, (255, 100, 100),
                        (player_screen_x - self.tile_size // 2,
                         player_screen_y - self.tile_size,
                         self.tile_size,
                         self.tile_size * 2))
        
        # Draw eyes
        pygame.draw.circle(screen, (0, 0, 0), (player_screen_x - 5, player_screen_y - 5), 2)
        pygame.draw.circle(screen, (0, 0, 0), (player_screen_x + 5, player_screen_y - 5), 2)
