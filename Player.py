import socket
import threading
from PlayerDeck import PlayerDeck
from SixCardGolf import SixCardGolf
import ast
#Global for all to access
server_ip = '10.120.70.133'
server_port = 50500


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
    




def sendAndRecieve(sock, message, ip, port):
    sock.sendto(message.encode('utf-8'), (ip, port))
    data, addr = sock.recvfrom(1024)
    return data, addr

def send_message(sock, message, ip, port):
    sock.sendto(message.encode('utf-8'), (ip, port))

def listen_for_peer_messages(client_ip, p_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((client_ip, int(p_port)))

    while True:
        data, addr = sock.recvfrom(1024)  
        decoded_message = data.decode('utf-8')
        print(decoded_message)
        return data, addr

def main():
    req = input('Send to tracker:\n\n')  # Prompt

    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if req.startswith('register'):
            _, _, ip, t_port, p_port = req.split()
            client.bind((ip, int(t_port)))
            data, _ = sendAndRecieve(client, req, server_ip, server_port)
            if data.decode('utf-8').startswith('SUCCESS'):
                listener_thread = threading.Thread(target=listen_for_peer_messages, args=(ip, p_port))
                listener_thread.daemon = True
                listener_thread.start()


            req = input('Send to server\n\n')
            client.close()

        elif req.startswith('query players') or req.startswith('query games') or req.startswith('de-register'):
            data, _ = sendAndRecieve(client, req, server_ip, server_port)
            print(data.decode('utf-8'))
            req = input('Send to server\n\n')
            client.close()

        elif req.startswith('start game'):
            _,_,player_name, num_players, num_holes = req.split(maxsplit = 4)

            data, _ = sendAndRecieve(client, req, server_ip, server_port)

            if data.decode('utf-8').startswith('SUCCESS'):
                _, players_in_game = data.decode('utf-8').split(':', 1)

                player_info_list = ast.literal_eval(players_in_game.strip())

                game_players = []

                print(player_info_list)

                # Parsing player information
                for player_info in player_info_list:
                    player_name = player_info[0].strip()
                    player_ip = player_info[1].strip()
                    player_port = int(player_info[2].strip())
                    game_players.append(Player(player_name, player_ip, player_port))

                #  initialized
                if len(game_players) == 0:
                    print("Error: No players were initialized. Cannot start the game.")
                    return

                #  Output initialized players
                SixCardGolf(num_players=len(game_players), num_holes=int(num_holes), players=game_players, dealer_client=client)

                # Exit  loop after game starts
                client.close()

        elif req == 'quit':
            client.close()
            break

        else:
            req = input('Send to server\n\n')


            
main()

# register Joe 10.120.70.112 50000 50001
# register Bob 10.120.70.120 50003 50004
# start game Joe 1 9


#general 3: 10.120.70.112
#general 4: 10.120.70.133
#general 5: 10.120.70.120