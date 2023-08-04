import socket
import rsa

public_key, private_key = rsa.newkeys(1024)
handler = None
# Create a socket object
client = socket.socket()

# Connect to the server at localhost:5555
client.connect(("192.168.1.64", 8888))

# Print success message when connected
print("Connection successful")

# Receive the PKCS1-encoded public key from the server
handler = rsa.PublicKey.load_pkcs1(client.recv(1024))
print(handler)
# Load the public key from the received data
client.send(public_key.save_pkcs1("PEM"))


print("Patner:" + rsa.decrypt(client.recv(1024), private_key).decode())



