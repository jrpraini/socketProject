from PlayerDeck import PlayerDeck

class Player:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.playerHand = PlayerDeck([])
        self.score = 0
            
    
    def __repr__(self):
        return f"Player({self.name}, {self.ip}, {self.port})"