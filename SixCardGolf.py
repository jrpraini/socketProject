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
        self.game()

    def current_game_state(self):
        self.game_state = ''

        self.game_state += f"\n\nDiscard: {self.discard[-1]}\n"
        for player in self.players:
            self.game_state += f"\n{player.name}'s Deck:\n\n{player.hand}\n\n"

        self.game_state += f'{self.players[self.current_player].name}\'s turn\n\n'
    
        return self.game_state


    def all_cards_face_up(self):
        for player in self.players:
            if not player.hand.all_cards_face_up():
                return False
        return True
        

    
    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            cards = [self.deck.draw() for _ in range(6)]  
            player.hand = PlayerDeck(cards)
            player.hand.flip_first_two()


    def game(self):
        while self.round <= self.num_holes:
            round_message = f"Round {self.round} has started."
            self.deal()  
            self.stock = self.deck.deck 

            discard_card = self.stock.pop()
            discard_card.flip()

            self.discard.append(discard_card) 

            # Play until all cards are face up for all players
            while not self.all_cards_face_up():
                for i, player in enumerate(self.players):
                    self.current_player = i
                    print(f"It's {player.name}'s turn.")
                    self.player_turn(player)

            self.calculate_scores()
            self.next_round()

        # self.end_game()


    def player_turn(self, player):
        send_to_all_players(self.socket, self.players, self.current_game_state()) 

        message = f"Your turn, {player.name}."
        message += f'\nYou have the option to draw from the stock, draw from discard pile, or swap a for another player\'s face down card.'
        message += f'Choose \'stock\' or \'discard\' to draw a card, or \'swap\' to swap a card with another player.'
        data = sendAndRecieve(self.socket, message, player.ip, player.port)

        choice = data.decode('utf-8')

        if choice == "stock":
            drawn_card = self.stock.pop()
        elif choice == "discard":
            drawn_card = self.discard.pop()
        elif choice == "swap":
            self.swap_card(player)
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
    
    def position_to_swap(self, current_player, swap_player):
        enemy_hand = swap_player.hand

        data = sendAndRecieve(self.socket, f"Enter the position of the card you want to swap: \n{enemy_hand}", current_player.ip, current_player.port)
        card_position = int(data.decode('utf-8'))

        if(card_position in range(6)):
            if swap_player.hand[card_position].face_up:
                send_message(self.socket, "You cannot swap a face up card. Please enter a valid card position.", current_player.ip, current_player.port)
                return self.position_to_swap(current_player, swap_player)
            else:
                swap_player.hand[card_position].flip()
                return card_position
        else:
            send_message(self.socket, "Invalid card position. Please enter a valid card position.", current_player.ip, current_player.port)
            return self.position_to_swap(current_player, swap_player)

    def player_position_to_swap(self, player):
        data = sendAndRecieve(self.socket, "Enter the position of the card you want to swap out.", player.ip, player.port)
        player_card_position = int(data.decode('utf-8'))

        if(player_card_position in range(6)):
            if not player.hand[player_card_position].face_up:
                player.hand[player_card_position].flip()
            return self.player_position_to_swap(player)
        else:
            send_message(self.socket, "Invalid card position. Please enter a valid card position.", player.ip, player.port)
            return self.player_position_to_swap(player)

    def swap_card(self, player):
        player_names = [p.name for p in self.players]
        player_names.remove(player.name)

        data = sendAndRecieve(self.socket, f"Enter the name of the player you want to swap with:\n {player_names}", player.ip, player.port)
        player_name = data.decode('utf-8')
        swap_player = None

        for p in self.players:
            if p.name in player_names:
                swap_player = p
            else:
                send_message(self.socket, "Invalid player name. Please enter a valid player name.", player.ip, player.port)
                swap_player = self.swap_card(player)
        
        enemy_card_position = self.position_to_swap(player, swap_player)
        player_card_position = self.player_position_to_swap(player)

        player.hand[player_card_position], swap_player.hand[enemy_card_position] = swap_player.hand[enemy_card_position], player.hand[player_card_position]

    

    # Move to the next round and rotate the dealer
    def next_round(self):
        print(f"Round {self.round} completed.")
        self.round += 1
        

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
