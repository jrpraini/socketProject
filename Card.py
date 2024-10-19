class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = 0
        self.hidden = True
        self.set_value()
    
    def set_value(self):
        if self.rank == "A":
            self.value = 1
        if self.rank == "2":
            self.value = -2
        elif self.rank in ["J", "Q"]:
            self.value = 10
        elif self.rank in ["K"]:
            self.value = 0
        else:
            self.value = int(self.rank)

    def __str__(self):
        if not self.hidden:
            return f" {self.rank}{self.suit}"
        else:
            return f"***"
    