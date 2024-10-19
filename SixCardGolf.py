import Deck
import Player
import socket

class SixCardGolf:
    def __init__(self, num_players, num_holes, players, dealer_client):
        self.deck = Deck.Deck()
        self.stock = []
        self.discard = []
        self.players = []
        self.current_player = 0
        self.round = 0
        self.game_over = False

    # def deal(self):


    def start_game(self):
        self.deck.shuffle()
        self.deal()
        self.play_game()
