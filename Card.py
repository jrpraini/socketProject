class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = None
        self.set_value()
        self.face_up = False # facing up or down flag 

    
    def set_value(self):
        if self.rank in ['J', 'Q', 'K']: # set face cards 10 points 
            self.value = 10 
        elif self.rank == 'A':
            self.value = 1 
        elif self.rank == '2':
            self.value = -2
        else:
            self.value = int(self.rank)  # 3 to 10 

    def flip(self):
        self.face_up = True #flip card 

    def __repr__(self):
       return f"{self.rank}{self.suit}"
       #return f"{self.rank} {self.suit} (value: {self.value})"
