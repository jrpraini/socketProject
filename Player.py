import socket
import threading
import SixCardGolf

#Global for all to access
server_ip = '10.120.70.112'
server_port = 50500

#Sends requests to tracker, prints response and returns data and addr for manipulation if needed
def sendAndRecieve(sock, message):
    sock.sendto(message.encode('utf-8'), (server_ip, server_port))
    data,addr = sock.recvfrom(1024)
    return data, addr

def listen_for_peer_messages(client_ip, p_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((client_ip, p_port))

    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
        return data, addr
    
def main():
    req = input('Send to tracker:\n\n') #Prompt

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
            _,_,player_name, num_players,num_holes,_ = req.split()
            data, _ = sendAndRecieve(client, req)

            if data.decode('utf-8').startswith('SUCCESS'):
                #Res format = f'SUCCESS: ${players_in_game}'
                _, players_in_game = data.decode('utf-8').split(':')
                players_in_game = players_in_game.strip().split(',')
                game = SixCardGolf.SixCardGolf(num_players, num_holes, players_in_game)

        elif req == 'quit':
            client.close()
            break

        else:
            req = input('Send to server\n\n')



main()