import socket

#Global for all to access
server_ip = '10.120.70.112'
server_port = 50500

#Sends requests to tracker, prints response and returns data and addr for manipulation if needed
def sendAndRecieve(sock, message):
    sock.sendto(message.encode('utf-8'), (server_ip, server_port))
    data,addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

    return data, addr

def main():
    req = input('Send to tracker:\n\n') #Prompt

    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if req.startswith('register'):
            _, _, ip, t_port, _ = req.split()
            client.bind((ip, int(t_port)))

            sendAndRecieve(client, req)
            req = input('Send to server\n\n')
        
        elif req.startswith('query players') or req.startswith('query games') or req.startswith('de-register'):
            sendAndRecieve(client, req)
            req = input('Send to server\n\n')
            client.close()

        elif req == 'quit':
            client.close()
            break

        else:
            req = input('Send to server\n\n')


main()

        