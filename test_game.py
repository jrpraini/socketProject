# test_game.py

# Import the SixCardGolf class and any other necessary classes
from SixCardGolf import SixCardGolf
from Deck import Deck

# Mock Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def arrange_hand(self):
        # Arranges the cards in two rows of three for display
        print(f" * ")

    def calculate_score(self):
        # Just a mock calculation for testing purposes
        self.score = sum(card.value for card in self.hand)
        print(f"{self.name}'s current score: ")

# Create mock players
player1 = Player('Player 1')
player2 = Player('Player 2')
player3 = Player('Player 3')

# Add them to a list
players = [player1, player2, player3]

# Initialize the SixCardGolf game
game = SixCardGolf(num_players=3, num_holes=3, players=players, dealer_client=0)

# Start the game
game.start_game()
