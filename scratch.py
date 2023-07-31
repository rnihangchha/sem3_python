import socket
import threading

host = "localhost"
port = 5555
server = socket.socket()
server.bind((host,port))
server.listen()
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message().encode())

def handling_clients(client):
    while True:
        try:
            msg = message = server.recv(1024).decode()
            if msg.startswith('KICKED'):
                if nicknames[clients.index(client)] == 'admin':

                    name_to_kick = msg[5:]
                    kick_user(name_to_kick)
            elif msg.startswith('BANNED'):

                if nicknames[clients.index(client)] == 'admin':

                    name_to_ban = msg[4:]
                    kick_user(name_to_ban)

                    with open('bans.txt', 'a') as f:
                        f.write(f"{name_to_ban}\n")
                    print(f"{name_to_ban} was banned")
                else:
                    client.send("Command was refused!".encode())
            else:

                broadcast(message)
        except:
            if client in clients:
                warn = clients.index(client)
                client.remove(client)
                client.close()
                nickname = nicknames[warn]
                broadcast(f"{nickname} left the chat :( !".encode())
                nicknames.remove(nickname)
                break

def recieving_clinets_socket_address():
    while True:
        client_socket, address = server.accept()
        print(f"connected with {str(address)}")
        client_socket.send('Nihangchha'.encode())
        nickname = client_socket.recv(1024).decode()

        with open('bans.txt','r') as f:
            ban = f.readlines()
        if nickname+ '\n'in ban:
            client_socket.send('BANNED'.encode())
            client_socket.close()
            continue
        if nickname == "admin":
            client_socket.send('PASS'.encode())
            password = client_socket.recv(2014).decode()
            if password != 'adminpass':
                client_socket.send("Refused".encode())
                client_socket.close()
                continue
        nickname.append(nicknames)
        clients.append(client_socket)

        print(f"Nickname of the {address} is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode())
        client_socket.send("[CONNECTED] tp server!".encode())

        threading.Thread(target=handling_clients, args=(client_socket,)).start()
def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("You have been kicked out by admin".encode())
        nicknames.remove(name)
        broadcast(f"{name} was kicked by kick by admin".encode())
print("Server is listening......")
recieving_clinets_socket_address()



















