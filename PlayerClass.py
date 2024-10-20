from PlayerDeck import PlayerDeck

class Player:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.hand = PlayerDeck([])
        self.score = 0  # For keeping track of scores
    
    def calculate_score(self):
        calculate = [0,1,2,3,4,5]

        if self.hand[0].suit == self.hand[3].suit:
            self.score += 0
            calculate.remove(0)
            calculate.remove(3)
        
        if self.hand[1].suit == self.hand[4].suit:
            self.score += 0
            calculate.remove(1)
            calculate.remove(4)
        
        if self.hand[2].suit == self.hand[5].suit:
            self.score += 0
            calculate.remove(2)
            calculate.remove(5)
        
        for i in calculate:
            self.score += self.hand[i].value

        return self.score
            
    
    def __repr__(self):
        return f"Player({self.name}, {self.ip}, {self.port})"