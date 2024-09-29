import socket
import threading

players = {}
games = {}

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
                    server.sendto(b"SUCCESS: Player registered\n", addr)

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
