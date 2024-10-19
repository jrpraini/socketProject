import socket 
import threading
import random

players = {}
games = {}
free_player = []

def handle_client(server, data, addr):
    try:
        message = data.decode('utf-8')

        print(f"Received: {message}")

        #Adds player to players dict and sends success back if register successful
        if message.startswith("register"):
            _, player_name, ip, t_port, p_port = message.split()
            if player_name in players:
                server.sendto(b"FAILURE: Duplicate player name\n", addr)
            else:
                matching_players = [player for player, info in players.items() if info[0] == ip and info[1] == t_port]

                if matching_players:
                    server.sendto(b"FAILURE: Socket in use\n", addr)
                else:
                    players[player_name] = (ip, t_port, p_port, "free")
                    free_player.push(player_name)

                    server.sendto(b"SUCCESS: Player registered\n", addr)

        elif message.startswith("start game"):
            players_in_game = []

            _, _, player_name, num_players, num_holes = message.split()

            if player_name not in players:
                server.sendto(b"FAILURE: Player not registered\n", addr)
                return
            
            if int(num_players) < 2 or int(num_players) > 4:
                server.sendto(b"FAILURE: Invalid number of players\n", addr) 
                return
            
            if len(players) < int(num_players):
                server.sendto(b"FAILURE: Not enough players registered\n", addr)
                return
            
            if int(num_holes) < 1 or int(num_holes) > 9:
                server.sendto(b"FAILURE: Invalid number of holes\n", addr)
                return
            
            dealer = players[player_name]
            dealer[3] = 'in-play'

            players_in_game.append((player_name, dealer[0], dealer[2]))

            for i in range(int(num_players)):
                player = free_player.pop(random.randint(0, len(free_player) - 1))
                players[player][3] = 'in-play'
                players_in_game.append(player, players[player][0], players[player][2])
            
            game_id = random.randint(1000, 9999)
            games[game_id] = (player_name, num_players, num_holes)

            response = f"SUCCESS: Game {game_id} started with players\n{players_in_game}"

            


        #Sends back all players currently in the player database
        elif message == "query players":
            if players:
                response = "\n".join([f"{name}: {info}" for name, info in players.items()])
            else:
                response = "No players registered"

            server.sendto(response.encode('utf-8'), addr)

        #Sends back all active games
        elif message.startswith("query games"):
            if games:
                response = "\n".join([f"{id}: {info}" for id, info in games.items()])
            else:
                server.sendto(b'No active games in progress', addr)

        #Removes the user, if exists, from the database
        elif message.startswith("de-register"):
            _, player_name = message.split()
            if player_name in players:
                del players[player_name]

                if player_name in free_player:
                    free_player.remove(player_name)

                server.sendto(b"SUCCESS: Player de-registered\n", addr)
            else:
                server.sendto("FAILURE: Player not found\n", addr)

        else:
            server.sendto(b'Invalid command, please try again', addr)

    except Exception as e:
        print(f"Error: {e}")

#Binds the tracker socket to ip and port, then whenever data is recieved, a client thread is initalized
def start_tracker(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('10.120.70.112', port))
    print(f"Tracker started on port {port}")
    

    while True:
        data, addr = server.recvfrom(1024)
        client_thread = threading.Thread(target=handle_client, args=(server, data, addr))
        client_thread.start()

if __name__ == "__main__":
    start_tracker(50500)
