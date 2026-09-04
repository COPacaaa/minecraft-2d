import pygame

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_small = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 48)
        
        self.block_names = {
            0: "Air (Empty)",
            1: "Dirt",
            2: "Grass",
            3: "Stone",
            4: "Sand",
            5: "Water",
        }
    
    def draw(self, screen, selected_block, paused, game_time):
        # Draw hotbar
        hotbar_y = self.height - 50
        pygame.draw.rect(screen, (50, 50, 50), (0, hotbar_y, self.width, 50))
        
        # Draw block selection indicators
        block_types = [1, 2, 3, 4]
        colors = {
            1: (139, 69, 19),    # Dirt
            2: (34, 139, 34),    # Grass
            3: (128, 128, 128),  # Stone
            4: (238, 213, 183),  # Sand
        }
        
        for i, block_type in enumerate(block_types):
            x = 20 + i * 60
            color = colors.get(block_type, (255, 255, 255))
            
            # Draw block box
            pygame.draw.rect(screen, color, (x, hotbar_y + 5, 40, 40))
            pygame.draw.rect(screen, (255, 255, 255) if block_type == selected_block else (0, 0, 0),
                           (x, hotbar_y + 5, 40, 40), 3)
            
            # Draw key number
            key_text = self.font_small.render(str(i + 1), True, (255, 255, 255))
            screen.blit(key_text, (x + 45, hotbar_y + 5))
        
        # Draw selected block name
        selected_name = self.block_names.get(selected_block, "Unknown")
        info_text = self.font_small.render(f"Selected: {selected_name}", True, (255, 255, 255))
        screen.blit(info_text, (20, 10))
        
        # Draw controls
        controls = [
            "WASD/Arrows: Move | Space: Jump",
            "1-4: Select Block | Left Click: Place | Right Click: Break",
            "ESC: Pause"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, (200, 200, 200))
            screen.blit(text, (20, 40 + i * 25))
        
        # Draw pause menu
        if paused:
            # Semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Pause text
            pause_text = self.font_large.render("PAUSED", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(pause_text, text_rect)
            
            resume_text = self.font_small.render("Press ESC to resume", True, (200, 200, 200))
            resume_rect = resume_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            screen.blit(resume_text, resume_rect)
