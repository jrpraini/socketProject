import socket
import threading
import random

# Database for players and games
players = {}
games = {}
free_players = []

def handle_client(server, data, addr):
    try:
        message = data.decode('utf-8')
        print(f"Received: {message}")

        # Register a player
        if message.startswith("register"):
            _, player_name, ip, t_port, p_port = message.split()
            if player_name in players:
                server.sendto(b"FAILURE: Duplicate player name\n", addr)
            else:
                # Check if the same IP and port combination already exists
                matching_players = [player for player, info in players.items() if info[0] == ip and info[1] == t_port]

                if matching_players:
                    server.sendto(b"FAILURE: Socket in use\n", addr)
                else:
                    players[player_name] = (ip, t_port, p_port, "free")
                    free_players.append(player_name)
                    server.sendto(b"SUCCESS: Player registered\n", addr)

        # Start a game
        elif message.startswith("start game"):
            _,_, player_name, num_players, num_holes = message.split(maxsplit=4)


            if player_name not in players:
                server.sendto(b"FAILURE: Player not registered\n", addr)
                return

            if int(num_players) < 1 or int(num_players) > 3:
                server.sendto(b"FAILURE: Invalid number of players\n", addr)
                return

            if len(free_players) < int(num_players):
                server.sendto(b"FAILURE: Not enough free players\n", addr)
                return

            if int(num_holes) < 1 or int(num_holes) > 9:
                server.sendto(b"FAILURE: Invalid number of holes\n", addr)
                return

            #Find dealer in free players, remove from free players and add to game
            dealer = players[player_name]
            free_players.remove(player_name)
            new_tuple = (dealer[0], dealer[1], dealer[2], "in-play")
            players[player_name] = new_tuple

            players_in_game = [(player_name, dealer[0], dealer[2])] 

            for _ in range(int(num_players)):
                new_player_name = free_players.pop(random.randint(0, len(free_players) - 1))
                old_player = players[new_player_name]
                new_player_tuple = (old_player[0], old_player[1], old_player[2], "in-play")
                players[new_player_name] = new_player_tuple
                players_in_game.append((new_player_name, new_player_tuple[0], new_player_tuple[2]))

            # Assign a unique game ID
            game_id = random.randint(1000, 9999)
            games[game_id] = (player_name, players_in_game, num_holes)
            
            response = f"SUCCESS: {players_in_game}"
            server.sendto(response.encode('utf-8'), addr)

        # Query all registered players
        elif message == "query players":
            if players:
                response = "\n".join([f"{name}: {info}" for name, info in players.items()])
            else:
                response = "No players registered"
            server.sendto(response.encode('utf-8'), addr)

        # Query all active games
        elif message == "query games":
            if games:
                response = "\n".join([f"Game ID {id}: Dealer: {info[0]}, Players: {info[1]}, Holes: {info[2]}" for id, info in games.items()])
            else:
                response = "No active games in progress"
            server.sendto(response.encode('utf-8'), addr)

        # De-register a player
        elif message.startswith("de-register"):
            _, player_name = message.split()
            if player_name in players:
                del players[player_name]
                if player_name in free_players:
                    free_players.remove(player_name)
                server.sendto(b"SUCCESS: Player de-registered\n", addr)
            else:
                server.sendto(b"FAILURE: Player not found\n", addr)

        else:
            server.sendto(b"Invalid command, please try again\n", addr)

    except Exception as e:
        print(f"Error: {e}")
        server.sendto(b"FAILURE: An error occurred while processing your request\n", addr)

# Binds the tracker socket to IP and port, then initializes a client thread when data is received
def start_tracker(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('10.120.70.133', port))
    print(f"Tracker started on port {port}")

    while True:
        data, addr = server.recvfrom(1024)
        client_thread = threading.Thread(target=handle_client, args=(server, data, addr))
        client_thread.start()

if __name__ == "__main__":
    start_tracker(50500)
