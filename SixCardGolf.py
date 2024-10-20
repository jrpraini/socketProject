import Deck
from PlayerDeck import PlayerDeck
from PlayerClass import Player
import random

def send_to_all_players(socket, players, message):
    for player in players:
        send_message(socket, message, player.ip, player.port)

def sendAndRecieve(sock, message, ip, port):
    sock.sendto(message.encode('utf-8'), (ip, port))
    data, addr = sock.recvfrom(1024)
    return data, addr

def send_message(sock, message, ip, port):
    sock.sendto(message.encode('utf-8'), (ip, port))

class SixCardGolf:
    def __init__(self, num_players, num_holes, players, dealer_client):
        self.deck = Deck.Deck()
        self.socket = dealer_client
        self.stock = []
        self.discard = []
        self.players = players  
        self.current_player = 0
        self.round = 1
        self.num_holes = num_holes
        self.num_players = num_players
        self.game_over = False
        self.game_state = ''
        self.start_game()

    def current_game_state(self):
        self.game_state = ''

        for player in self.players:
            self.game_state += f"\n{player.name}'s Deck:\n\n{player.hand}\n\n"
            self.game_state += f"Discard: {self.discard[-1]}\n\n"
            self.game_state += f'Player {self.players[self.current_player].name}\'s turn\n\n'
        
        return self.game_state


    def all_cards_face_up(self):
        for player in self.players:
            if not player.all_cards_face_up():
                return False
        return True
        

    
    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            cards = [self.deck.draw() for _ in range(6)]  
            player.hand = PlayerDeck(cards)
            player.hand.flip_first_two()


    def start_game(self):
        while self.round <= self.num_holes:
            round_message = f"Round {self.round} has started."
            self.deal()  
            self.stock = self.deck.deck[:]  
            discard_card = self.stock.pop().flip()
            self.discard.append(discard_card) 

            self.game_state = self.current_game_state()

            round_message += self.game_state
            send_to_all_players(self.socket, self.players, round_message) 

        #     # Play until all cards are face up for all players
        #     while not self.all_cards_face_up():
        #         for i, player in enumerate(self.players):
        #             self.current_player = i
        #             print(f"It's {player.name}'s turn.")
        #             self.player_turn(player)

        #     self.calculate_scores()
        #     self.next_round()

        # self.end_game()

    # Player's turn logic
    def player_turn(self, player):
        print(f"{player.name}, your hand:")
        for idx, card in enumerate(player.hand):
            print(card)

        print(f"{player.name}, you have the option to draw from the stock or discard pile.")
        choice = input("Choose 'stock' or 'discard': ").strip().lower()

        if choice == "stock":
            drawn_card = self.stock.pop()
        elif choice == "discard":
            drawn_card = self.discard.pop()
        else:
            print("Invalid choice, you must pick either 'stock' or 'discard'.")
            return self.player_turn(player)

        print(f"{player.name} drew: {drawn_card.rank} of {drawn_card.suit} (value: {drawn_card.value})")

        for idx, card in enumerate(player.hand):
            if card.face_up:
                print(f"Card {idx}: {card.rank} of {card.suit} (Value: {card.value}) - FACE UP")
            else:
                print(f"Card {idx}: Face Down")

        card_to_replace = int(input("Select the card position (0-5) to replace, or -1 to discard the drawn card: "))

        if card_to_replace in range(6):
            replaced_card = player.hand[card_to_replace]
            player.hand[card_to_replace] = drawn_card
            player.hand[card_to_replace].flip() 
            self.discard.append(replaced_card)
            print(f"Replaced {replaced_card.rank} of {replaced_card.suit} with {drawn_card.rank} of {drawn_card.suit}")
        else:
            self.discard.append(drawn_card)
            print(f"{player.name} discarded {drawn_card.rank} of {drawn_card.suit}")

    # Move to the next round and rotate the dealer
    def next_round(self):
        print(f"Round {self.round} completed.")
        self.round += 1
        if self.round <= self.num_holes:
            self.rotate_dealer()

    # Calculate the score of each player at the end of the round
    def calculate_scores(self):
        for player in self.players:
            player.calculate_score()  # Calculate the score for each player
            print(f"{player.name}'s score: {player.score}")

    # End the game after all rounds
    def end_game(self):
        print("Game over. Final scores:")
        for player in self.players:
            print(f"{player.name}: {player.score}")

        winner = min(self.players, key=lambda p: p.score)
        print(f"The winner is {winner.name} with {winner.score} points!")
