import random
import time

import pygame

import Button
import menu
import Player


def run_game():

    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("BlackJack")

    # Set up the font
    font = pygame.font.Font(None, 36)

    # Bet
    global bet
    bet = 50 # Default bet size

    # Game state
    global finished
    finished = False

    '''
    Individual cards
    '''
    class Card:

        def __init__(self, suit, value):
            self.suit = suit
            self.value = int(value)
            self.image = Card.setImage(self)
            self.front = self.image

        def __repr__(self):
            return f"{self.value} of {self.suit}"

        def setImage(self):
            if (self.suit == "Hearts"):
                return pygame.image.load(f"assets/BlackJack/Hand Drawn Cards/Hearts/{self.value}h.png")
            elif (self.suit == "Diamonds"):
                return pygame.image.load(f"assets/BlackJack/Hand Drawn Cards/Diamonds/{self.value}d.png")
            elif (self.suit == "Clubs"):
                return pygame.image.load(f"assets/BlackJack/Hand Drawn Cards/Clubs/{self.value}c.png")
            else:
                return pygame.image.load(f"assets/BlackJack/Hand Drawn Cards/Spades/{self.value}s.png")

        def flipCard(self):
            back = pygame.image.load('assets/BlackJack/Hand Drawn Cards/Back Blue.png') # back image
            if self.image == self.front:
                self.image = back
            else:
                self.image = self.front


    '''
    Create a new deck
    '''
    class Deck:

        def __init__(self):
            self.cards = []
            self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            self.values = [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
            ]

            self.fillDeck()

        def fillDeck(self):
            for suit in self.suits:
                for value in self.values:
                    self.cards.append(Card(suit, value))

        def shuffle(self):
            random.shuffle(self.cards)

        def deal(self):
            if len(self.cards) == 0:
                self.fillDeck()
                self.shuffle()
            return self.cards.pop()

    '''
    Player hand
    '''
    class Hand:

        def __init__(self):
            self.cards = []
            self.full_value = False

        def add_card(self, card):
            self.cards.append(card)

        def get_value(self):
            value = 0
            aces = 0
            for card in self.cards:
                if 2 <= card.value <= 10:
                    value += card.value
                elif card.value in [11, 12, 13]:
                    value += 10
                elif card.value == 1: # Ace
                    aces += 1
                    value += 11

            while value > 21 and aces:
                value -= 10
                aces -= 1

            return value

        def get_display_value(self):
            if self.full_value:
                return self.get_value()
            else:
                value = self.cards[0].value
                if 2 <= value <= 10:
                    return value
                elif value in [11, 12, 13]:
                    return 10
                elif value == 1: # Ace
                    return 11

        def __repr__(self):
            return f"Hand value: {self.get_value()} with cards {self.cards}"

    '''
    Initial play of the game
    '''
    # Create a deck and shuffle it
    deck = Deck()
    deck.shuffle()

    # Deal two cards to the player and the dealer
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.cards[1].flipCard()

    '''
    Game Loop
    '''
    while True:
    # Draw the screen
    # Background
        background_image = pygame.image.load('assets/BlackJack/background.jpg')
        background_image = pygame.transform.scale(background_image,
                                                  screen.get_size())
        screen.blit(background_image, (0, 0))

        # Buttons
            # Load button images
        backButton = pygame.image.load(
            'assets/random buttons/png/Black-Icon/MediumArrow-Left.png')
        dealB = pygame.image.load('assets/BlackJack/Buttons/deal1.png')
        hitB = pygame.image.load('assets/BlackJack/Buttons/hit1.png')
        standB = pygame.image.load('assets/BlackJack/Buttons/stand1.png')
        doubleB = pygame.image.load('assets/BlackJack/Buttons/double1.png')
        splitB = pygame.image.load('assets/BlackJack/Buttons/split1.png')
        addB = font.render("+", False, (255, 255, 255))
        betI = font.render(str(bet), False, (255, 255, 255))
        balI = font.render(f"${Player.getBalance()}", False, (255, 255, 255))
        subB = font.render("-", False, (255, 255, 255))
        ext = font.render("-", False, (255, 255, 255))
        hand_valueP = font.render(f"{player_hand.get_value()}", False, (255, 255, 255))
        hand_valueD = font.render(f"{dealer_hand.get_display_value()}", False, (255, 255, 255))
            # Create all the buttons
        buttons = [
            Button.ImageButton(hand_valueD, 0.33, 0.25, 0.08),
            Button.ImageButton(hand_valueP, 0.5, 0.75, 0.08),
            Button.ImageButton(backButton, 0.03, 0.04, 0.07),
            Button.ImageButton(dealB, 0.10, 0.8, 0.1),
            Button.ImageButton(hitB, 0.80, 0.8, 0.1),
            Button.ImageButton(standB, 0.90, 0.8, 0.1),
            Button.ImageButton(doubleB, 0.45, 0.9, 0.1),
            Button.ImageButton(splitB, 0.55, 0.9, 0.1),
            Button.ImageButton(addB, 0.715, 0.94, 0.1),
            Button.ImageButton(betI, 0.79, 0.95, 0.05),# Not actually a button lol
            Button.ImageButton(balI, 0.50, 0.97, 0.08),# This either lol
            Button.ImageButton(subB, 0.845, 0.94, 0.1),
            Button.ImageButton(ext, 0.849, 0.94, 0.1)
        ]

        # Draw current player hand
        player_drawn_hand = []
        for count, card in enumerate(player_hand.cards):
            x = 0.45 + (0.05 * count) # Not buttons lol, I should change the name
            player_drawn_hand.append(Button.ImageButton(card.image, x, 0.57, 0.25))
        # Draw current dealer hand
        dealer_drawn_hand = []
        for count, card in enumerate(dealer_hand.cards):
            x = 0.45 + (0.05 * count) # Still not buttons, just dynamic images
            dealer_drawn_hand.append(Button.ImageButton(card.image, x, 0.25, 0.25))

        # Draw all the cards
        Button.drawButtons(screen, player_drawn_hand)
        Button.drawButtons(screen, dealer_drawn_hand)
        # Draw all the buttons
        Button.drawButtons(screen, buttons)

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        # Change bet ammout if balance goes below bet ammount
        if Player.Balance < bet:
            bet = Player.Balance

        '''
        Game event handling methods
        '''
        # Handle player hitting
        def hit(player_hand, dealer_hand, multiplier):
            global finished, bet
            if (not finished):
                player_hand.add_card(deck.deal())
                if player_hand.get_value() > 21:
                    print("Player busts! Dealer wins!")
                    # TODO Display on screen you lost
                    Player.subFromBalance(bet*multiplier)
                    finished = True
                elif player_hand.get_value() == 21 and dealer_hand.get_value() == 21:
                    dealer_hand.cards[1].flipCard()
                    dealer_hand.full_value = True
                    finished = True
                    print("Push! It's a tie!")
                    # TODO Display on screen you tied

        # Handle player standing
        def stand(player_hand, dealer_hand, multiplier):
            global finished, bet
            if (not finished):
                finished = True
                if player_hand.get_value() == 21 and dealer_hand.get_value() == 21:
                    dealer_hand.cards[1].flipCard()
                    dealer_hand.full_value = True
                    finished = True
                    print("Push! It's a tie!")
                    # TODO Display on screen you tied
                else:
                    dealer_hand.cards[1].flipCard()
                    dealer_hand.full_value = True
                    if dealer_hand.get_value() < 17:
                        while 21 > dealer_hand.get_value() < 17:
                            dealer_hand.add_card(deck.deal())
                        # Check special case wins
                        if dealer_hand.get_value() > 21:
                            if player_hand.get_value == 21:
                                Player.addToBalance(bet+(bet/2)*multiplier)
                                print("1Dealer busts! Player wins!")
                                # TODO Display on screen you won
                            else:
                                Player.addToBalance(bet*multiplier)
                                print("2Dealer busts! Player wins!")
                                # TODO Display on screen you won
                        else:
                            checkWinner(player_hand, dealer_hand, multiplier)
                    else:
                        checkWinner(player_hand, dealer_hand, multiplier)
        
        # Check if there is a winner
        def checkWinner(player_hand, dealer_hand, multiplier):
            global bet
            if player_hand.get_value() > dealer_hand.get_value():
                if player_hand.get_value() == 21:
                    Player.addToBalance(bet+(bet/2)*multiplier) # 2.5x win
                    print("Player wins!")
                    # TODO Display on screen you won
                else:
                    Player.addToBalance(bet*multiplier) # 2x win
                    print("Player wins!")
                    # TODO Display on screen you won
            elif player_hand.get_value() < dealer_hand.get_value():
                Player.subFromBalance(bet*multiplier)
                print("Dealer wins!")
                # TODO Display on screen you lost
            else:
                print("Push! It's a tie!")
                # TODO Display on screen you tied

        def pressedButton(button, filePath):
            button.image = pygame.image.load(filePath)
            button.draw(screen, screen.get_width(), screen.get_height())
            pygame.display.flip()
            pygame.time.delay(100)

        '''
        Check player activity
        '''
        for event in pygame.event.get():
            # Exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                menu.run_menu()    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Check if any buttons are clicked
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                    # Back Button
                        if button.image == backButton:
                            pygame.quit()
                            menu.run_menu()
                        # Deal Button
                        elif button.image == dealB:
                            filePath = 'assets/BlackJack/Buttons/deal2.png'
                            pressedButton(button, filePath)
                            if (finished and bet > 0):
                                # Reset and deal new cards
                                player_hand = Hand() # New player hand
                                player_hand.add_card(deck.deal())
                                player_hand.add_card(deck.deal())
                                dealer_hand = Hand() # New dealer hand
                                dealer_hand.add_card(deck.deal())
                                dealer_hand.add_card(deck.deal())
                                dealer_hand.cards[1].flipCard()
                                dealer_hand.full_value = False
                                finished = False
                            elif (bet <= 0):
                                print("You can't play if you're broke!")
                                # Display u cant play if you're broke
                        # Hit Button
                        elif button.image == hitB:
                            filePath = 'assets/BlackJack/Buttons/hit2.png'
                            pressedButton(button, filePath)
                            hit(player_hand, dealer_hand, 1)
                        # Stand Button
                        elif button.image == standB:
                            filePath = 'assets/BlackJack/Buttons/stand2.png'
                            pressedButton(button, filePath)
                            stand(player_hand, dealer_hand, 1)
                        # Double Button
                        elif button.image == doubleB:
                            filePath = 'assets/BlackJack/Buttons/double2.png'
                            pressedButton(button, filePath)
                            hit(player_hand, dealer_hand, 2)
                            stand(player_hand, dealer_hand, 2)
                        # Split Button
                        elif button.image == splitB:
                            filePath = 'assets/BlackJack/Buttons/split2.png'
                            pressedButton(button, filePath)
                            if (not finished):
                                print("split logik")
                        # Add to bet Button
                        elif button.image == addB:
                            if (finished):
                                if(bet+50 >= Player.getBalance()):
                                    bet = Player.getBalance()
                                else:
                                    bet += 50
                        # Subtracte from bet Button
                        elif button.image == subB:
                            if (finished):
                                if(bet-50 <= 0):
                                    bet = 0
                                else:
                                    bet -= 50

'''
Of course, this is just a starting point, and you'll need to add more
features to create a fully functional blackjack game.
Some ideas for additional features include:
  -Standing: Allow the player to stand and end their turn

  -Doubling down: Allow the player to double their bet and receive one more card.

  -Splitting: Allow the player to split their hand into two separate hands
  if their initial cards have the same value.

  -Insurance: Offer the player insurance if the dealer's up card is an Ace.

  -Dealer's turn: Implement the dealer's turn, where they draw cards until
  they reach a certain value or bust.

  -Money system 
  *Bet amt on screen with + and - buttons next to it change bet


'''
