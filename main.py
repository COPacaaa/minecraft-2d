import pygame
import sys
from game import Game

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 32

# Colors
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Minecraft")
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
    
    running = True
    while running:
        clock.tick(60)  # 60 FPS
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        game.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
