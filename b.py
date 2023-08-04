import socket
import threading
import rsa

HOST = "192.168.1.64"
PORT = 8888

PUBLIC_KEY_SIZE = 2048


def receive_messages(client_socket, private_key):
    try:
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            else:
                # Decrypt the message using the client's private key
                message = rsa.decrypt(encrypted_message, private_key).decode('utf-8')
                print(message)
    except Exception as e:
        print(f"Error receiving message: {str(e)}")
    finally:
        client_socket.close()


def send_messages(client_socket, username, public_partner):
    try:
        while True:
            message = input("MESSAGE >> ")

            if message.lower() == "quit":
                # Send the encrypted "quit" message to the server
                client_socket.send(rsa.encrypt(message.encode('utf-8'), public_partner))
                break
            else:
                # Send the encrypted message to the server
                client_socket.send(rsa.encrypt(f"{username}: {message}".encode('utf-8'), public_partner))
    except Exception as e:
        print(f"Error sending message: {str(e)}")
    finally:
        client_socket.close()


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # Generate the client's RSA key pair
        public_key, private_key = rsa.newkeys(PUBLIC_KEY_SIZE)

        # Send the client's public key to the server
        client_socket.send(public_key.save_pkcs1("PEM"))

        # Receive the server's public key
        public_partner = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))

        username = input("Enter your username: ")
        # Send the encrypted username to the server
        client_socket.send(rsa.encrypt(username.encode('utf-8'), public_partner))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, private_key))
        send_thread = threading.Thread(target=send_messages, args=(client_socket, username, public_partner))

        receive_thread.start()
        send_thread.start()

        receive_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        client_socket.close()


if __name__ == '__main__':
    main()
