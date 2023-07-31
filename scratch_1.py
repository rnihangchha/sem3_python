import rsa
import socket
import threading

public_key, private_key = rsa.newkeys(1024)
handler = None

# Define the function to handle each client connection
def handle(client):
    try:
        op = client.send(rsa.encrypt("Hey what's up how u been doing".encode(), handler))

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        client.close()

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket option to reuse the address to avoid "address already in use" error
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address (localhost:5555)
s.bind(("192.168.1.64", 8888))

# Listen for incoming connections
s.listen()

print("Server Listening")

# Set the handler to use the public key for sending to clients


# Start an infinite loop to accept incoming connections
while True:
    # Accept a client connection and get the client socket and address
    client, addr = s.accept()
    print(f"NEW {addr}")
    client.send(public_key.save_pkcs1("PEM"))
    handler = rsa.PublicKey.load_pkcs1(client.recv(1024))
    # Create a new thread to handle the client
    threading.Thread(target=handle, args=(client,)).start()
