import socket, os

import threading

IP = "192.168.1.66"
PORT = 5555
clients = []
nicknames = []
def broadcast(msg):
    for client in clients:
        print(client)
        client.send(bytes(msg.encode('ascii')))

def handle_client(client):
    while True:
        try:
            msg = message = client.recv(2048).decode('ascii')
            if msg.startswith('KICK'):
                if nickname[client.index(client)] == 'admin':

                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command was refused!'.encode('ascii'))
            elif msg.startswith('BAN'):
                name_to_ban = msg.decode('ascii')[4:]
                kick_user(name_to_ban)
                with open('bans.txt', 'a') as f:
                    f.write(f'{name_to_ban}\n')

                print(f'{name_to_ban} was banned')
            else:

                broadcast(msg)
        except:
            if client in clients:
                index = client.index(client)
                client.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} [LEFT THE CHAT :()]'.encode('ascii'))
                nicknames.remove(nickname)
                break

def start_server():
    print(f"Succesfully connected\n[LISTENING] on {IP}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] from {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        print(os.getcwd())
        if not os.path.exists('bans.txt'):
            with open('bans.txt', 'w') as f:
                pass  # This will create an empty 'bans.txt' file if it doesn't exist.
            bans = []
        else:
            with open('bans.txt', 'r') as f:
                bans = f.readlines()

        if nickname + '\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        if nickname == "admin":
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname of the client is {nickname}!")
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('Your were kicked by the {ADMIN}'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an ADMIN'.encode('ascii'))
if __name__ == "__main__":
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((IP,PORT))
    server.listen(10)
    start_server()