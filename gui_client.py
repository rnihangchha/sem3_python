import socket
import threading
import rsa

host = "localhost"
port = 8888

public_key, private_key = rsa.newkeys(2048)
public_partner = None

def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            else:
                # Decrypt the message using the client's private key
                message = rsa.decrypt(encrypted_message, private_key)
                print(message.decode("utf-8"))
        except Exception as e:
            print(f"Error receiving message: {str(e)}")
            break

def send_messages(client_socket, username):
    while True:
        try:
            message = input("MESSAGE >> ")
            
            if message == "quit":
                # Send the encrypted "quit" message to the server
                encrypted_message = rsa.encrypt(message.encode("utf-8"), public_partner)
                client_socket.send(encrypted_message)
                client_socket.close()
                break
            else:
                # Send the encrypted message to the server
                encrypted_message = rsa.encrypt(f"{username}: {message}".encode("utf-8"), public_partner)
                client_socket.send(encrypted_message)
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            break

def main():
    try:
        global public_partner
        client_socket = socket.socket()
        client_socket.connect((host, port))
        
        # Send the client's public key to the server
        client_socket.send(public_key.save_pkcs1().decode("utf-8"))
        username = input("Enter your username: ")
        encrypt_usr = rsa.encrypt(username, public_partner)
        client_socket.send(encrypt_usr.encode("utf-8"))

        # Receive the server's public key
        server_public_key = rsa.PublicKey.load_pkcs1(client_socket.recv(1024).decode("utf-8"))
        
        
        public_partner = server_public_key

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket, username))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        client_socket.close()

if __name__ == '__main__':
    main()
