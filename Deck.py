import random
import Card

class Deck:
    def __init__(self):
        self.deck = []
        self.initialize()

    def initialize(self):
        suits = ['H', 'D', 'C', 'S']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card.Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

    def peek(self):
        return self.deck[-1]
    
    def reset(self):
        self.deck = []
        self.initialize()

    def __str__(self):
        return "\n".join([str(card) for card in self.deck])