class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = None
        self.set_value()
        self.face_up = False

    
    def set_value(self):
        if self.rank in ['J', 'Q']:
            self.value = 10 
        elif self.rank == 'A':
            self.value = 1 
        elif self.rank == '2':
            self.value = -2
        elif self.rank == 'K':
            self.value = 0
        else:
            self.value = int(self.rank)

    def flip(self):
        self.face_up = True #flip card 

    def __str__(self):
        if self.face_up:
            return f" {self.rank}{self.suit}"
        else:
            return "***"
