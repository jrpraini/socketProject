import socket
import threading
from SixCardGolf import SixCardGolf

#Global for all to access
server_ip = '10.120.70.133'
server_port = 50500

#Sends requests to tracker, prints response and returns data and addr for manipulation if needed
def sendAndRecieve(sock, message):
    sock.sendto(message.encode('utf-8'), (server_ip, server_port))
    data,addr = sock.recvfrom(1024)
    return data, addr

def listen_for_peer_messages(client_ip, p_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((client_ip, int(p_port)))

    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
        print(f"Message from peer {addr}: {data.decode('utf-8')}")
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
            _,_,player_name, num_players,num_holes = req.split(maxsplit = 4)

            data, _ = sendAndRecieve(client, req)

            if data.decode('utf-8').startswith('SUCCESS'):
                _, players_in_game = data.decode('utf-8').split(':',1)
                players_in_game = players_in_game.strip().split(',')
                print(f'Players in game: {players_in_game}')
                req = input('Send to server\n\n')
            else:
                print(data.decode('utf-8'))
                req = input('Send to server\n\n')

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