import random
from collections import Counter
from itertools import combinations, filterfalse

import pygame

import Button
import menu
import Player

# Constants
screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)  # Fullscreen mode
NUM_PLAYERS = 5
NUM_CARDS = 2
CARD_WIDTH = 20  # Adjust based on your card image size
CARD_HEIGHT = 30  # Adjust based on your card image size

# Global Variables
deck = None
players = None
middle_cards = None
game_state = 0
cards_flipped_flags = [True] * NUM_PLAYERS
checked_players = [False] * NUM_PLAYERS
raising = False
bet = 50
pot = 0
reset_game = False
raised = False


        # i might have an idea
# Example usage:
# hand = [Card('Hearts', 10), Card('Hearts', 13), Card('Hearts', 12), Card('Hearts', 11), Card('Hearts', 14)]
# print(evaluate_hand(hand))  # Should return (10, hand) for Royal Flush


class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = self.setImage()
        self.front = self.image

    def setImage(self):
        if (self.suit == "Hearts"):
            return pygame.image.load(
                f"assets/BlackJack/Hand Drawn Cards/Hearts/{self.value}h.png")
        elif (self.suit == "Diamonds"):
            return pygame.image.load(
                f"assets/BlackJack/Hand Drawn Cards/Diamonds/{self.value}d.png"
            )
        elif (self.suit == "Clubs"):
            return pygame.image.load(
                f"assets/BlackJack/Hand Drawn Cards/Clubs/{self.value}c.png")
        else:
            return pygame.image.load(
                f"assets/BlackJack/Hand Drawn Cards/Spades/{self.value}s.png")

    def flipCard(self):
        back = pygame.image.load(
            'assets/BlackJack/Hand Drawn Cards/Back Purple.png')  # back image
        if self.image == self.front:
            self.image = back
        else:
            self.image = self.front

class playerClass:
    def __init__(self):
        self.hand = []
        self.folded = False

    def foldPlayer(self):
        self.folded = True
        self.hand = []


class Deck:

    def __init__(self):
        self.cards = []
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
                       ]  # Use integers for values from 2 to 13 ('Ace' is 1)
        self.fillDeck()
        self.shuffle()  # Shuffle cards right after building

    def fillDeck(self):
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num=1):
        if len(self.cards) <= num:
            self.fillDeck()
            self.shuffle()
        return [self.cards.pop() for _ in range(num)]

def draw_hand(screen, hand, y_position):
    drawn_hand = []
    for count, card in enumerate(hand):
        x_position = 0.45 + (0.05 * count)
        drawn_hand.append(
            Button.ImageButton(card.image, x_position, y_position, 0.25))
    # Draw all the cards on the screen
    Button.drawButtons(screen, drawn_hand)


def draw(self, screen):
    color = self.color_active if self.is_hovered() else self.color_inactive
    pygame.draw.rect(screen, color, self.rect)
    text_surface = self.font.render(self.text, True,
                                    (255, 255, 255))  # White text
    screen.blit(text_surface, self.rect.move(10, 10))


def is_hovered(self):
    return self.rect.collidepoint(pygame.mouse.get_pos())


def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered():
        if self.action:
            self.action()

def initPlayers(deck, NUM_CARDS):
    newPlayers = [playerClass() for i in range(NUM_PLAYERS)]
    for i, player in enumerate(newPlayers):
        player.hand = deck.deal(NUM_CARDS)
        if i != 2 :
            for card in player.hand:
                card.flipCard()
    return newPlayers

def initMiddleCards(deck):
    new_middle_cards = deck.deal(5)  # Deal five community cards
    for card in new_middle_cards:
        card.flipCard()
    return new_middle_cards

'''
Game Functions
'''
def getWinner(players, middle_cards):
    winner = players[2]
    bestScore = -1
    for player in players:
        # Check if player has a hand
        if not player.folded:
            score = evaluate_hand(player.hand, middle_cards)
            if player != players[2]:
                for card in player.hand:
                    card.flipCard()
        else:
            score = -1
        if score > bestScore:
            bestScore = score
            winner = player
    return winner
        
def evaluate_hand(hand, middle_cards):
    all_cards = hand + middle_cards # Combine hands
    possible_hands = combinations(all_cards, 5) # Create all possible 5-card combinations
    best_score = 0
    # Evaluate all possible 5-card combinations
    for possible_hand in possible_hands:
        score = evaluate_five_card_hand(possible_hand)
        if score > best_score:
            best_score = score
    return best_score

def evaluate_five_card_hand(hand):
    values = sorted(
        [card.value for card in hand],
        reverse=True)
    suits = [card.suit for card in hand]
    value_counts = Counter(values)
    counts = sorted(value_counts.values(), reverse=True)
    unique_values = sorted(value_counts.keys(), reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = (len(unique_values) == 5
                   and (unique_values == [1, 13, 12, 11, 10]
                        or all(unique_values[i] == unique_values[i + 1] + 1
                               for i in range(4))))
    if is_flush and is_straight and unique_values[0] == 1:
        return (10)  # Royal Flush
    elif is_flush and is_straight:
        return (9)  # Straight Flush
    elif counts == [4, 1]:
        return (8)  # Four of a Kind
    elif counts == [3, 2]:
        return (7)  # Full House
    elif is_flush:
        return (6)  # Flush
    elif is_straight:
        return (5)  # Straight
    elif counts == [3, 1, 1]:
        return (4)  # Three of a Kind
    elif counts == [2, 2, 1]:
        return (3)  # Two Pair
    elif counts == [2, 1, 1, 1]:
        return (2)  # One Pair
    else:
        return (1)  # High Card

def get_weights_for_game_state(game_state):
    weights_map = {
        # Check, Fold, Raise chances
        0: [0.7, 0.2, 0.1],  # Pre-flop
        1: [0.5, 0.2, 0.3],  # After the flop
        2: [0.4, 0.1, 0.3],  # After the turn
        3: [0.3, 0.05, 0.5]  # After the river
    }
    return weights_map.get(game_state)

def player_decision(game_state):
    weights = get_weights_for_game_state(game_state)
    if weights:
        return random.choices([0, 1, 2], weights)[0]
    
def run_game():

    # Globals
    global game_state, cards_flipped_flags, raising, bet, pot, players, middle_cards
    global deck, reset_game, raised, checked_players
    font = pygame.font.Font(None, 36) # Set up the font
    
    '''
    Initial play of the game
    '''
    # Initialize the deck here
    deck = Deck()

    # Create all player hands
    players = initPlayers(deck, NUM_CARDS) 
    checked_players = [False] * NUM_PLAYERS
    
    # Create middle cards
    middle_cards = initMiddleCards(deck)

    '''
    Game Loop
    '''
    while True:
        pygame.init()

        # Load and scale background image to fit screen
        background_image = pygame.image.load(
            'assets/Poker/poker_background.jpg').convert()
        background_image = pygame.transform.scale(background_image,
                                                  screen.get_size())
        screen.blit(background_image,
                    (0, 0))  # Blit the scaled background image

        all_in = pygame.image.load('assets/Poker/Buttons/poker_all_in.png')
        Call = pygame.image.load('assets/Poker/Buttons/poker_call.png')
        Check = pygame.image.load('assets/Poker/Buttons/poker_check.png')
        Raise = pygame.image.load('assets/Poker/Buttons/poker_raise.png')
        Fold = pygame.image.load('assets/Poker/Buttons/poker_fold.png')
        Bet = pygame.image.load('assets/Poker/Buttons/poker_bet.png')
        addB = font.render("+", False, (255, 255, 255))
        betI = font.render(str(bet), False, (255, 255, 255))
        balI = font.render(f"${Player.getBalance()}", False, (255, 255, 255))
        potI = font.render(f"${pot}", False, (255, 255, 255))
        subB = font.render("-", False, (255, 255, 255))
        ext = font.render("-", False, (255, 255, 255))
        backButton = pygame.image.load(
            'assets/random buttons/png/Black-Icon/MediumArrow-Left.png')

        buttons = [
            Button.ImageButton(all_in, 0.16, 0.1, 0.16),
            Button.ImageButton(backButton, 0.03, 0.04, 0.07),
            Button.ImageButton(balI, 0.25, 0.09, 0.1),
            Button.ImageButton(potI, 0.495, 0.32, 0.1)
        ]
        # If at start of game then use Call instead of Check
        if (not raising):
            buttons.append(Button.ImageButton(Fold, 0.25, 0.93, 0.16))
            buttons.append(Button.ImageButton(Raise, 0.75, 0.93, 0.16))
            if game_state == 0 or raised:
                buttons.append(Button.ImageButton(Call, 0.50, 0.93, 0.16))
            else:
                buttons.append(Button.ImageButton(Check, 0.50, 0.93, 0.16))
        else:
            buttons.append(Button.ImageButton(Bet, 0.50, 0.93, 0.16))
            buttons.append(Button.ImageButton(addB, 0.615, 0.93, 0.1))
            buttons.append(Button.ImageButton(betI, 0.69, 0.94, 0.05))
            buttons.append(Button.ImageButton(subB, 0.745, 0.93, 0.1))
            buttons.append(Button.ImageButton(ext, 0.749, 0.93, 0.1))
        
        Button.drawButtons(screen, buttons) # Draw the buttons

        # Game state middle cards logic
        flipped_cards = 0
        if game_state == 1:
            flipped_cards = 3
        elif game_state == 2:
            flipped_cards = 4
        elif game_state >= 3:
            flipped_cards = 5

        for i in range(flipped_cards):
            if cards_flipped_flags[i]: # Check if not flipped
                middle_cards[i].flipCard() # Flips
                cards_flipped_flags[i] = False # Marks as flipped

        # Draw middle cards
        drawn_middle_cards = []
        for i, card in enumerate(middle_cards):
            x = 0.40 + (0.05 * i) 
            drawn_middle_cards.append(
                Button.ImageButton(card.image, x, 0.50, 0.15))
        Button.drawButtons(screen, drawn_middle_cards)

        # Draw all player hands
        player_pos = {
            # x cord, y cord
            0: (0.23, 0.35), # Top left
            1: (0.23, 0.64), # Bottom left
            2: (0.4875, 0.71), # Middle (Main Player)
            3: (0.74, 0.64), # Bottom right
            4: (0.74, 0.35) # Top right
        }
        drawn_player_cards = []
        for j, player in enumerate(players):
            for k, card in enumerate(player.hand):
                x, y = player_pos[j]
                x += (0.03 * k)
                y += (0.01 * k)
                drawn_player_cards.append(Button.ImageButton(card.image, x, y, 0.15))
        Button.drawButtons(screen, drawn_player_cards)

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        # Run the game for the oppenent players
        def play_op_players(players, checked_players, game_state):
            global raised, pot, reset_game
            for i, player in enumerate(players):
                if player != players[2]:
                    if not player.folded:
                        players_folded = sum(player.folded for player in players if player != players[i])
                        if players_folded != 4:
                            play = player_decision(game_state)
                            if play == 0: # Check
                                if raised or game_state == 0:
                                    pot += 50
                                checked_players[i] = True
                            elif play == 1: # Fold
                                player.foldPlayer()
                                checked_players[i] = True
                            elif play == 2: # Raise
                                pot += random.randint(50, 250)
                                raised = True
                        else:
                            checked_players[i] = True
                    else:
                        checked_players[i] = True
            ops_folded = sum(player.folded for player in players if player != players[2])
            if ops_folded == 4:
                Player.addToBalance(pot)
                reset_game = True
                

        # Create a new game
        def newGame():
            global game_state, cards_flipped_flags, raising, bet, pot, players, middle_cards
            global deck, reset_game, raised, checked_players
            # Reset all variables to defaults
            game_state = 0
            cards_flipped_flags = [True] * 5
            checked_players = [False] * 5
            raising = False
            bet = 50 
            pot = 0
            reset_game = False
            raised = False
            players = initPlayers(deck, NUM_CARDS) 
            middle_cards = initMiddleCards(deck)

        # Check if need to reset game
        if reset_game:
            pygame.time.delay(2000)
            newGame()
            reset_game = False

        # Change button pressed image
        def pressedButton(button, filePath):
            button.image = pygame.image.load(filePath)
            button.draw(screen, screen.get_width(), screen.get_height())
            pygame.display.flip()
            pygame.time.delay(100)

        # Handle Player Buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                menu.run_menu()  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse position
                mouse_pos = pygame.mouse.get_pos()
                # Check if any buttons are clicked
                for button in buttons:
                    if button.is_clicked(mouse_pos):
                        # All In Button
                        # The "All In" button is clicked. This means the player is betting all their chips, 
                        # so the entire bet amount is deducted from their balance.
                        if button.image == all_in:
                            filePath = 'assets/Poker/Buttons/poker_all_in2.png'
                            pressedButton(button, filePath)
                            if Player.Balance > 0:
                                pot += Player.Balance
                                # Deduct all chips
                                Player.subFromBalance(Player.Balance) 
                                for i, player in enumerate(players):
                                    choice = random.randint(1, 2)
                                    if (i > 2 or i < 2): # Avoid Main Player
                                        if choice == 1:
                                            pot += 500
                                        else:
                                            player.foldPlayer()
                                game_state = 3
                                if getWinner(players, middle_cards) == players[2]:
                                    Player.addToBalance(pot)
                                reset_game = True
                                
                        # Fold Button
                        # The "Fold" button is clicked. The player decides to fold, meaning they quit the current hand.
                        # No chips are deducted, but the cards need to be redealt for the next hand.
                        elif button.image == Fold:
                            filePath = 'assets/Poker/Buttons/poker_fold2.png'
                            pressedButton(button, filePath)
                            players[2].foldPlayer()
                            playing = True
                            while (playing):
                                checked_players = [False] * NUM_PLAYERS
                                checked_players[2] = True
                                play_op_players(players, checked_players, game_state)
                                if not checked_players.__contains__(False):
                                    game_state += 1
                                if game_state == 4:
                                    if getWinner(players, middle_cards) == players[2]:
                                        Player.addToBalance(pot)
                                    reset_game = True
                                    playing = False

                        # Check Button
                        # The "Check" button is clicked. This means the player doesn't want to bet any more chips.
                        # If all players check, then the next 1 of 2 cards that are non-revealed (the community cards) is revealed.
                        elif button.image == Check:
                            filePath = 'assets/Poker/Buttons/poker_check2.png'
                            pressedButton(button, filePath)
                            if Player.Balance > 0:
                                checked_players = [False] * 5
                                print("cehck")
                                checked_players[2] = True
                                play_op_players(players, checked_players, game_state)
                                if not checked_players.__contains__(False):
                                    game_state += 1
                                if game_state == 4:
                                    if getWinner(players, middle_cards) == players[2]:
                                        Player.addToBalance(pot)
                                    reset_game = True
                                    
                        # Call Button
                        # The "Call" button is clicked. The player matches the current bet (called "calling"), 
                        # and the bet amount is deducted from their balance.
                        elif button.image == Call:
                            filePath = 'assets/Poker/Buttons/poker_call2.png'
                            pressedButton(button, filePath)
                            if Player.Balance > 0:
                                checked_players = [False] * 5
                                if raised: # Reset raised
                                    raised = False
                                bet = 50
                                pot += bet
                                Player.subFromBalance(bet)
                                checked_players[2] = True
                                play_op_players(players, checked_players, game_state)
                                if not checked_players.__contains__(False):
                                    game_state += 1
                                if game_state == 4:
                                    if getWinner(players, middle_cards) == players[2]:
                                        Player.addToBalance(pot)
                                    reset_game = True
                                
                        # Raise Button
                        # The "Raise" button is clicked. The player increases the bet by the bet amount, 
                        # and the amount is deducted from their balance.
                        elif button.image == Raise:
                            filePath = 'assets/Poker/Buttons/poker_raise2.png'
                            pressedButton(button, filePath)
                            if Player.Balance > 0:
                                raising = True
                                raised = True
                        # Part of Raise
                        elif button.image == Bet:
                            filePath = 'assets/Poker/Buttons/poker_bet2.png'
                            pressedButton(button, filePath)
                            raising = False
                            pot += bet # Adjust pot by bet
                            Player.subFromBalance(bet)
                            play_op_players(players, checked_players, game_state)
                        # Part of Raise
                        elif button.image == addB:
                            if(bet+50 >= Player.getBalance()):
                                bet = Player.getBalance()
                            else:
                                bet += 50
                        # Part of Raise
                        elif button.image == subB:
                            if(bet-50 <= 0):
                                bet = 0
                            else:
                                bet -= 50
                                
                        # Back Button
                        # The "Back" button is clicked. The game exits and returns to the main menu.
                        elif button.image == backButton:
                            pygame.quit()  # Quit the game
                            menu.run_menu()  # Return to the menu
