import random
from Card import Card

class Deck:
    def __init__(self):
        self.deck = []
        self.initialize()
        self.shuffle()

    def initialize(self):
        suits = ['H', 'D', 'C', 'S']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    # Add the draw method to take the top card from the deck
    def draw(self):
        if len(self.deck) == 0:
            raise ValueError("No more cards to draw from the deck")
        return self.deck.pop()  # Remove and return the top card from the deck

    def __repr__(self):
        return f"Deck of {len(self.deck)} cards"
