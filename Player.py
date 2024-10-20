import socket
import threading
from SixCardGolf import SixCardGolf

#Global for all to access
server_ip = '10.120.70.133'
server_port = 50500


def sendAndRecieve(sock, message):
    sock.sendto(message.encode('utf-8'), (server_ip, server_port))
    data, addr = sock.recvfrom(1024)
    return data, addr

def listen_for_peer_messages(client_ip, p_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((client_ip, int(p_port)))

    while True:
        data, addr = sock.recvfrom(1024)  
        return data, addr

class Player:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.hand = []  
        self.score = 0  # For keeping track of scores
    
    def calculate_score(self):
        
        self.score = sum(card.value for card in self.hand if card.face_up)
    
    def __repr__(self):
        return f"Player({self.name}, {self.ip}, {self.port})"

def main():
    req = input('Send to tracker:\n\n')  # Prompt

    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if req.startswith('register'):
            _, _, ip, t_port, p_port = req.split()
            client.bind((ip, int(t_port)))
            data, _ = sendAndRecieve(client, req)
            if data.decode('utf-8').startswith('SUCCESS'):
                listener_thread = threading.Thread(target=listen_for_peer_messages, args=(ip, p_port))
                listener_thread.daemon = True
                listener_thread.start()


            req = input('Send to server\n\n')
            client.close()

        elif req.startswith('query players') or req.startswith('query games') or req.startswith('de-register'):
            data, _ = sendAndRecieve(client, req)
            print(data.decode('utf-8'))
            req = input('Send to server\n\n')
            client.close()

        elif req.startswith('start game'):
            _,_,player_name, num_players,num_holes = req.split(maxsplit = 4)

            data, _ = sendAndRecieve(client, req)

            if data.decode('utf-8').startswith('SUCCESS'):
                _, players_in_game = data.decode('utf-8').split(':', 1)
                
                
                player_data_str = players_in_game.split('Players:')[-1]
                player_data_str = player_data_str.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace("'", "")
                
                # Debugging the cleaned player string
                print(f"Cleaned Player Data String: {player_data_str}")

                
                player_info_list = player_data_str.split(',')

                game_players = []

                # Parsing player information
                for i in range(0, len(player_info_list), 3):  # (name, ip, port) 
                    try:
                        player_name = player_info_list[i].strip()
                        player_ip = player_info_list[i+1].strip()
                        player_port = player_info_list[i+2].strip()
                        game_players.append(Player(player_name, player_ip, int(player_port)))
                    except (IndexError, ValueError) as e:
                        print(f"Error parsing player information: {e}")
                        continue

                #  initialized
                if len(game_players) == 0:
                    print("Error: No players were initialized. Cannot start the game.")
                    return

                #  Output initialized players
                print(f"Initialized Players: {game_players}")

                game = SixCardGolf(num_players=len(game_players), num_holes=int(num_holes), players=game_players, dealer_client=0)

                # Start  game
                print("Starting the game with the selected players...")
                game.start_game()

                # Exit  loop after game starts
                break

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