import socket
import threading
import sys
import rsa

host = "192.168.1.64"
port = 8888

public_key, private_key = rsa.newkeys(2048)
public_patner = None

class LoginServer:
    def __init__(self):
        self.users = []
        self.clients = []
        try:
            self.server = socket.socket()
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            print(f"Server is starting......\n[LISTENING] on {host}:{port}")
            try:
                self.server.listen()
            except Exception as e:
                print("ERROR LISTENING FOR CLIENT: " + str(e))
                sys.exit(1)
        except Exception as e:
            print("SOCKET ERROR:" + str(e))
            sys.exit(1)

    def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                # Encrypt the message using the client's public key
                encrypted_msg = rsa.encrypt(message.encode("utf-8"), client.public_key)
                client.socket.send(encrypted_msg)

    def handle_client(self, client_socket):
        try:
            username = client_socket.recv(1024).decode("utf-8")
            username_encrypted =  rsa.decrypt(username, private_key)
            print(username_encrypted)
            self.broadcast(f"\n{username} joined the chat\n", client_socket)

            while True:
                encrypted_message = client_socket.recv(1024)
                
                if not encrypted_message:
                    break  # Empty message indicates client disconnection
                else:
                    # Decrypt the message using the server's private key
                    message = rsa.decrypt(encrypted_message, private_key)
                    message = message.decode("utf-8")
                    if message == "quit":
                        self.broadcast(f"{username} LEFT THE CHAT!", client_socket)
                        client_socket.send("{quit}".encode("utf-8"))
                        client_socket.close()
                        self.clients.remove(client_socket)
                    else:
                        self.broadcast(f"{username}: {message}", client_socket)

        except Exception as e:
            print(f"[EXCEPTION] due to {e}")

    def start_server(self):
        print("I am here")
        while True:
            print("iam here")
            try:
                client_socket, address = self.server.accept()
                print(f"[NEW CONNECTION] from {address}!")
                client_socket.send(public_key.save_pkcs1("PEM"))
                public_patner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))
                print("hello")
            except KeyboardInterrupt:
                it = input("YOU REALLY WANNA TERMINATE THE SERVER? (y/n)")
                if it.lower() == "y":
                    break
                elif it.lower() == "n":
                    continue

            except Exception as e:
                print("Error accepting client connection " + str(e))
                sys.exit(1)
            
            self.clientObj(client_socket)

    def clientObj(self, client_socket):
        self.clients.append(client_socket)

    def client_thread(self, client):
        try:
            threadObj = threading.Thread(target=self.handle_client, args=(client.socket,))
            threadObj.start()
        except Exception as e:
            print("ERROR CREATING THREAD: " + str(e))
            sys.exit(1)


if __name__ == '__main__':
    final_server = LoginServer()
    final_server.start_server()
