import Deck
import random

class SixCardGolf:
    def __init__(self, num_players, num_holes, players, dealer_client):
        self.deck = Deck.Deck()  # Assuming Deck.Deck() provides a shuffled deck of cards
        self.stock = []
        self.discard = []
        self.players = players  
        self.current_player = 0
        self.dealer_client = dealer_client
        self.round = 1
        self.num_holes = num_holes
        self.num_players = num_players
        self.game_over = False

    def all_cards_face_up(self):
        # Check if all cards for all players are face-up
        return all(all(card.face_up for card in player.hand) for player in self.players)

    
    def deal(self):
        self.deck.shuffle()  # Shuffle the deck before dealing in each round
        for player in self.players:
            player.hand = [self.deck.draw() for _ in range(6)]  
            face_up_indices = random.sample(range(6), 2)  # Pick two random cards to be face-up
            for index in face_up_indices:
                player.hand[index].flip()  # Flip two random cards face-up

    # Start the game
    def start_game(self):
        self.deal()  # Deal cards to each player for the first round
        self.play_game()  # Begin the game logic

    def play_game(self):
        while self.round <= self.num_holes:
            print(f"Round {self.round} begins.")
            
            # Reset the deck, shuffle, and reset stock and discard piles
            self.deck = Deck.Deck()  # Create a new deck for each round
            self.deal()  
            self.stock = self.deck.deck[:]  
            self.discard.append(self.stock.pop())  

            # Play until all cards are face up for all players
            while not self.all_cards_face_up():
                for i, player in enumerate(self.players):
                    self.current_player = i
                    print(f"It's {player.name}'s turn.")
                    self.player_turn(player)

            self.calculate_scores()
            self.next_round()

        self.end_game()

    # Player's turn logic
    def player_turn(self, player):
        print(f"{player.name}, your hand:")
        for idx, card in enumerate(player.hand):
            if card.face_up:
                print(f"Card {idx}: {card.rank}{card.suit} (Value: {card.value}) - FACE UP")
            else:
                print(f"Card {idx}: ***")

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

    # Rotate the dealer for the next round
    def rotate_dealer(self):
        print(f"The dealer rotates.")
        self.dealer_client = (self.dealer_client + 1) % self.num_players

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
