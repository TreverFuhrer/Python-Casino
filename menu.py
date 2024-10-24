import sys  # Standard library import

import pygame  # Third-party import

import BlackJack  # Local application import
import Button
import Player
import Poker  # Local application import


def run_menu():
    # Initialize Pygame

    # Initialize Pygame
    pygame.init()

    # Draw background
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Crown of Chance")
    background_image = pygame.image.load('assets/Main/menu2.jpg').convert()
    background_image = pygame.transform.scale(background_image,
                                              screen.get_size())
    screen.blit(background_image,(0, 0))
    font = pygame.font.Font(None, 36)

    while True:
        # Draw logo and buttons
        casino_logo = pygame.image.load('assets/Main/Casino Title.png')
        black_jack = pygame.image.load('assets/Main/blackjack_button.png')
        poker = pygame.image.load('assets/Main/poker_button.png')
        player_balance = font.render(f"${Player.getBalance()}", False, (255, 255, 255))
        buttons = [
            Button.ImageButton(casino_logo, 0.495, 0.20, 0.9),
            Button.ImageButton(black_jack, 0.40, 0.65, 0.4),
            Button.ImageButton(poker, 0.18, 0.46, 0.4),
            Button.ImageButton(player_balance, 0.70, 0.70, 0.2)
        ]
        Button.drawButtons(screen, buttons)

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Detect Pressed Buttons
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        if button.image == black_jack:
                            BlackJack.run_game()
                        elif button.image == poker:
                            Poker.run_game()
