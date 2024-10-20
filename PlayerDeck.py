#Player Deck for Six Card Golf
class PlayerDeck:
    def __init__(self, cards):
        self.hand = cards
        self.score = 0
        self.flip_first_two()

    def flip_first_two(self):
        self.hand[0].flip()
        self.hand[1].flip()
        
    def all_cards_face_up(self):
        return all(card.face_up for card in self.hand)

    def __str__(self):
        return f"{self.hand[0]} {self.hand[1]} {self.hand[2]}\n{self.hand[3]} {self.hand[4]} {self.hand[5]}\n"
            
