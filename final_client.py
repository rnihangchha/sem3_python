import socket
import os
import threading

IP = "192.168.1.66"
PORT = 5555

nickname = input("Enter your nickname: ")
if nickname == 'admin':
    password = input(f'Enter the password {nickname}: ')
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((IP,PORT))
print("SUCESSFULLY CONNECTED")

stop_thread = False
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(message.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused !  Wrong password")
                        stop_thread = True
                elif next_message == 'BAN':
                    print("Connection refuse or aborted forcefully because of ban")
                    client.close()
                    break
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break
def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}:{input("")}'
        if message[len(nickname) + 2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname) + 2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))
            else:
                print("Command can only be executed by the admin!")
        else:
            client.send(message.encode('ascii'))


        



   

    
receive_thread =threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()