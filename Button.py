import pygame


class ImageButton:
    def __init__(self, image, x_ratio, y_ratio, size_ratio):
        self.image = image  # Button image
        self.x_ratio = x_ratio  # Percentage X position
        self.y_ratio = y_ratio  # Percentage Y position
        self.size_ratio = size_ratio  # Percentage size
        self.scaled_image = None  # Placeholder
        self.rect = None  # Placeholder

    def draw(self, screen, screen_width, screen_height):
        # Scale the image
        button_size = int(self.size_ratio *
                          min(screen_width, screen_height))

        # Make image proportional
        w, h = self.image.get_size()
        aspect_ratio = w / h
        if aspect_ratio > 1:
            # Image is wider than tall
            width = button_size
            height = int(button_size / aspect_ratio)
        else:
            # Image is taller or square
            width = int(button_size * aspect_ratio)
            height = button_size

        self.scaled_image = pygame.transform.scale(self.image,
                                                   (width, height))

        # Calculate position
        x = int(self.x_ratio * screen_width)
        y = int(self.y_ratio * screen_height)

        # Update buttons colision box
        # isClicked() detects if mouse clicked within this box's area
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        # Draw the image at the position
        screen.blit(self.scaled_image, (x - width // 2, y - height // 2))

    # Check if the button is clicked
    def is_clicked(self, mouse_pos):
        return bool(self.rect and self.rect.collidepoint(mouse_pos))
        

def drawButtons(screen, buttons):
    screen_width, screen_height = screen.get_size()
    for button in buttons:
        button.draw(screen, screen.get_width(), screen.get_height())