import socket
import threading

# Global state of the tracker
players = {}  # Dictionary to store registered players

# Handle client requests
def handle_client(conn, addr):
    print(f"Connection established with {addr}")
    while True:
        try:
            # Receive message from player
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")

            # Process the player's message
            if message.startswith("register"):
                _, player_name, ip, t_port, p_port = message.split()
                if player_name in players:
                    conn.send("FAILURE: Duplicate player name\n".encode('utf-8'))
                else:
                    players[player_name] = (ip, t_port, p_port, "free")
                    conn.send("SUCCESS: Player registered\n".encode('utf-8'))

            elif message == "query players":
                if players:
                    response = "\n".join([f"{name}: {info}" for name, info in players.items()])
                else:
                    response = "No players registered"
                conn.send(response.encode('utf-8'))

            elif message.startswith("de-register"):
                _, player_name = message.split()
                if player_name in players:
                    del players[player_name]
                    conn.send("SUCCESS: Player de-registered\n".encode('utf-8'))
                else:
                    conn.send("FAILURE: Player not found\n".encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()

def start_tracker(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Tracker started on port {port}")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_tracker(5000)  # Tracker listening on port 5000
