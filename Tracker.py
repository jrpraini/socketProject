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
                
                matching_players = [player for player, info in players.items() if info[0] == ip and info[1] == t_port]

                if matching_players:
                    server.sendto(b"FAILURE: Socket in use\n", addr)
                else:
                    players[player_name] = (ip, t_port, p_port, "free")
                    free_players.append(player_name)
                    print(f"Player {player_name} added to free_players. Current free players: {free_players}")

                    server.sendto(b"SUCCESS: Player registered\n", addr)

        # Start a game
        elif message.startswith("start game"):
            _,_, player_name, num_players, num_holes = message.split(maxsplit=4)
            print(f"Start game command received: {player_name}, {num_players}, {num_holes}")

            if player_name not in players:
                server.sendto(b"FAILURE: Player not registered\n", addr)
                return

            if int(num_players) < 2 or int(num_players) > 4:
                print("Invalid number of players")
                server.sendto(b"FAILURE: Invalid number of players\n", addr)
                return

            if len(free_players) < int(num_players):
                print(f"Free players: {free_players}")
                print(f"Number of free players: {len(free_players)}")
                print("Not enough free players available")  #checks , free players not being reassigned after the game ends 
                server.sendto(b"FAILURE: Not enough free players\n", addr)
                return

            if int(num_holes) < 1 or int(num_holes) > 9:
                print("Invalid number of holes")
                server.sendto(b"FAILURE: Invalid number of holes\n", addr)
                return

            
            dealer = players[player_name]
            players[player_name] = (dealer[0], dealer[1], dealer[2], "in-play")

            # Select random free players to participate in the game
            players_in_game = [(player_name, dealer[0], dealer[2])]  # Add dealer to the game
            print(f"Dealer assigned: {player_name}")

            for _ in range(int(num_players) - 1):
                player = free_players.pop(random.randint(0, len(free_players) - 1))
                print(f"Selected player: {player}")
                players[player] = (players[player][0], players[player][1], players[player][2], "in-play")
                players_in_game.append((player, players[player][0], players[player][2]))

            # Assign a unique game ID
            game_id = random.randint(1000, 9999)
            games[game_id] = (player_name, players_in_game, num_holes)

            response = f"SUCCESS: Game started with ID {game_id}. Players: {players_in_game}"
            print(f"Game successfully started with ID {game_id}")
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


def start_tracker(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('192.168.0.155', port))
    print(f"Tracker started on port {port}")

    while True:
        data, addr = server.recvfrom(1024)
        client_thread = threading.Thread(target=handle_client, args=(server, data, addr))
        client_thread.start()

if __name__ == "__main__":
    start_tracker(50500)
