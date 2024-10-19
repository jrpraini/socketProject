import Deck
import Player

class SixCardGolf:
    def __init__(self, num_players, num_holes, players):
        self.deck = Deck.Deck()
        self.stock = []
        self.discard = []
        self.players = []
        self.current_player = 0
        self.round = 0
        self.game_over = False

    def deal(self):
        for player in self.players:
            for _ in range(6):
                player.hand.append(self.deck.deal())
