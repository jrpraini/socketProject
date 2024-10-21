from Deck import Deck
from PlayerDeck import PlayerDeck
from PlayerClass import Player

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
        self.deck = Deck()
        self.socket = dealer_client
        self.stock = []
        self.discard = []
        self.players = players  
        self.player_to_start = 0
        self.current_player = 0
        self.round = 1
        self.num_holes = num_holes
        self.num_players = num_players
        self.game_over = False
        self.game_state = ''
        self.roundInProgress = True
        self.game()

    def current_game_state(self):
        self.game_state = ''

        for player in self.players:
            self.game_state += f"\n{player.name}'s Deck:\n\n{player.playerHand}\n\n"

        self.game_state += f"\n\nDiscard: {self.discard[-1]}\n"
        self.game_state += f'{self.players[self.current_player].name}\'s turn\n\n'
    
        return self.game_state


    def all_cards_face_up(self, player):
        return player.playerHand.all_cards_face_up()
        

    
    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            cards = [self.deck.draw() for _ in range(6)]  
            player.playerHand = PlayerDeck(cards)
            player.playerHand.flip_first_two()

    
    def game(self):
        print("Starting game...")
        while self.round <= self.num_holes:
            self.deal()  
            self.stock = self.deck.deck 
            discard_card = self.stock.pop()
            discard_card.flip()

            self.discard.append(discard_card) 

            #Play until one player has all cards face up
            while self.roundInProgress:
                self.player_turn(self.players[self.current_player])
                for player in self.players:
                    if(self.all_cards_face_up(player)):
                        self.roundInProgress = False                
                self.current_player = (self.current_player + 1) % self.num_players

            self.calculate_scores()
            self.next_round()
        self.end_game()
        return

        

    def player_turn(self, player):
        send_to_all_players(self.socket, self.players, self.current_game_state()) 

        message = f"INPUT:\nYour turn, {player.name}."
        message += f'\n\nYour hand:\n{player.playerHand}\n\n'
        message += f'\nChoose \'stock\' to draw from the stock\n\'discard\' to draw a card from discard pile\n\'swap\' to swap a card with another player.\n'

        data,_ = sendAndRecieve(self.socket, message, player.ip, player.port)
        choice = data.decode('utf-8')

        while choice not in ['stock', 'discard', 'swap']:
            data, _ = sendAndRecieve(self.socket, "INPUT:\nInvalid choice. Please enter a valid choice.", player.ip, player.port)
            choice = data.decode('utf-8')

        if choice == "stock":
            self.select_stock(player, self.stock.pop())
        elif choice == "discard":
            self.select_discard(player, self.discard.pop())
        else:
            self.swap_card(player)
        
        return

    def select_stock(self, player, drawn_card):
        drawn_card.flip()
        send_message(self.socket, f"{player.name} drew {drawn_card} from the stock.", player.ip, player.port)
        data,_ = sendAndRecieve(self.socket, f"INPUT:\nSelect the card position (0-5) to replace, or -1 to discard the drawn card: \n{player.playerHand}", player.ip, player.port)
        card_to_replace = int(data.decode('utf-8'))

        while card_to_replace not in range(6) and card_to_replace != -1:
            send_message(self.socket, "Invalid card position. Please enter a valid card position.", player.ip, player.port)
            data,_ = sendAndRecieve(self.socket, f"INPUT:\nSelect the card position (0-5) to replace, or -1 to discard the drawn card: \n{player.playerHand}", player.ip, player.port)
            card_to_replace = int(data.decode('utf-8'))
        
        if card_to_replace in range(6):
            if not player.playerHand.hand[card_to_replace].face_up:
                player.playerHand.hand[card_to_replace].flip()
                swap_card = player.playerHand.hand[card_to_replace]
                player.playerHand.hand[card_to_replace] = drawn_card
                self.discard.append(swap_card)
                send_to_all_players(self.socket, self.players, f"{player.name} swapped {swap_card} for {drawn_card}")
                return
        
        else:
            self.discard.append(drawn_card)
            send_to_all_players(self.socket, self.players, f"{player.name} discarded {drawn_card}")
            return


    def select_discard(self, player, drawn_card):
        data,_ = sendAndRecieve(self.socket, f"INPUT:\nSelect the card position (0-5) to replace \n{player.playerHand}", player.ip, player.port)
        card_to_replace = int(data.decode('utf-8'))

        while card_to_replace not in range(6):
            send_message(self.socket, "Invalid card position. Please enter a valid card position.", player.ip, player.port)
            data,_ = sendAndRecieve(self.socket, f"INPUT:\nSelect the card position (0-5) to replace \n{player.playerHand}", player.ip, player.port)
            card_to_replace = int(data.decode('utf-8'))

        if card_to_replace in range(6):
            if not player.playerHand.hand[card_to_replace].face_up:
                player.playerHand.hand[card_to_replace].flip()
                swap_card = player.playerHand.hand[card_to_replace]
                player.playerHand.hand[card_to_replace] = drawn_card
                self.discard.append(swap_card)
                send_to_all_players(self.socket, self.players, f"{player.name} swapped {swap_card} for {drawn_card}")
                return
                
    def get_valid_card_position(self, prompt, player, card_range, check_face_down=False):
        data, _ = sendAndRecieve(self.socket, prompt, player.ip, player.port)
        card_position = int(data.decode('utf-8'))

        while not(card_position in card_range and (not check_face_down or not player.playerHand.hand[card_position].face_up)):
            invalid_msg = "\nInvalid card position. Please enter a valid card position.\n"
            send_message(self.socket, invalid_msg, player.ip, player.port)
            data, _ = sendAndRecieve(self.socket, prompt, player.ip, player.port)
            card_position = int(data.decode('utf-8'))

        return card_position

    def position_to_swap(self, current_player, swap_player):
        enemy_hand = swap_player.playerHand
        prompt = f"INPUT:\nEnter the position of the card you want to swap for: \n{enemy_hand}\nThe card must be face down."
        
        card_position = self.get_valid_card_position(prompt, current_player, range(6), check_face_down=True)
        swap_player.playerHand.hand[card_position].flip()
        return card_position

    def player_position_to_swap(self, player):
        prompt = f"INPUT:\nEnter the position of the card you want to swap out: \n{player.playerHand}"
        card_position = self.get_valid_card_position(prompt, player, range(6))
        
        if not player.playerHand.hand[card_position].face_up:
            player.playerHand.hand[card_position].flip()

        return card_position

    def swap_card(self, player):
        player_names = [p.name for p in self.players if p.name != player.name]

        while True:
            data, _ = sendAndRecieve(self.socket, f"INPUT:\nEnter the name of the player you want to swap with:\n {player_names}", player.ip, player.port)
            player_name = data.decode('utf-8')
            swap_player = next((p for p in self.players if p.name == player_name), None)

            if swap_player:
                break
            else:
                send_message(self.socket, "Invalid player name. Please enter a valid player name.", player.ip, player.port)

        enemy_card_position = self.position_to_swap(player, swap_player)
        player_card_position = self.player_position_to_swap(player)

        # Swap the cards
        player.playerHand.hand[player_card_position], swap_player.playerHand.hand[enemy_card_position] = (
            swap_player.playerHand.hand[enemy_card_position],
            player.playerHand.hand[player_card_position]
        )
        
        send_message(self.socket, f"Swapped {player.playerHand.hand[player_card_position]} with {swap_player.playerHand.hand[enemy_card_position]}", player.ip, player.port)
        send_message(self.socket, f"Player {player.name} just swapped {swap_player.playerHand.hand[enemy_card_position]} for {player.playerHand.hand[player_card_position]}", swap_player.ip, swap_player.port)

    # Move to the next round and rotate the dealer
    def next_round(self):
        print(f"Round {self.round} completed.")
        self.round += 1
        self.deck = Deck()
        self.stock = []
        self.discard = []
        self.roundInProgress = True
        self.player_to_start = (self.player_to_start + 1) % self.num_players
        self.current_player = self.player_to_start

        

    # Calculate the score of each player at the end of the round
    def calculate_scores(self):
        for player in self.players:
            player.score += player.playerHand.calculate_score()
            send_to_all_players(self.socket, self.players, f"{player.name}'s score: {player.score}")
        return

    # End the game after all rounds
    def end_game(self):
        send_to_all_players(self.socket, self.players, "Game over!")
        for player in self.players:
            send_to_all_players(self.socket, self.players, f"{player.name}'s final score: {player.score}")

        winner = min(self.players, key=lambda p: p.score)
        
        send_to_all_players(self.socket, self.players, f"The winner is {winner.name} with a score of {winner.score}!")

        return