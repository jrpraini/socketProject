#Player Deck for Six Card Golf
class PlayerDeck:
    def __init__(self, cards):
        self.hand = cards
    
    def calculate_score(self):
        score = 0

        calculate = [0,1,2,3,4,5]

        if self.hand[0].suit == self.hand[3].suit:
            calculate.remove(0)
            calculate.remove(3)
        
        if self.hand[1].suit == self.hand[4].suit:
            calculate.remove(1)
            calculate.remove(4)
        
        if self.hand[2].suit == self.hand[5].suit:
            calculate.remove(2)
            calculate.remove(5)
        
        for i in calculate:
            score += self.hand[i].value
        return score

    def flip_first_two(self):
        self.hand[0].flip()
        self.hand[1].flip()
        
    def all_cards_face_up(self):
        return all(card.face_up for card in self.hand)

    def __str__(self):
        return f"{self.hand[0]} {self.hand[1]} {self.hand[2]}\n{self.hand[3]} {self.hand[4]} {self.hand[5]}\n"
            
