import socket
import threading
from PlayerClass import Player
from SixCardGolf import SixCardGolf
import ast

#Global for all to access
server_ip = '10.120.70.133'
server_port = 50500
    
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

        if decoded_message.startswith('INPUT'):
            req = input('')
            send_message(sock, req, addr[0], addr[1])

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
                _, game_id, players_in_game = data.decode('utf-8').split(':')

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

                data, _ = sendAndRecieve(client, f'end {int(game_id)} {game_players[0].name}', server_ip, server_port)

                if data.decode('utf-8').startswith('SUCCESS'):
                    print('Game ended successfully')
                client.close()

        elif req == 'quit':
            client.close()
            break

        else:
            req = input('Send to server\n\n')


            
main()

# register Joe 10.120.70.112 50000 50001
# register Bob 10.120.70.120 50003 50004
# register Billy 10.120.70.120 50005 50006
# register Grace 10.120.70.112 50007 50008
# start game Joe 1 1
# start Grace 1 1


#general 3: 10.120.70.112
#general 4: 10.120.70.133
#general 5: 10.120.70.120