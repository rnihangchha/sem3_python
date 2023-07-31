import sqlite3
import hashlib
import socket
import threading


HOST = "localhost"
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 9999))
s.listen(5)
client_socket = []
user = []


def broadcast(message):
    for cl in client_socket:
        cl.send(message)


def handle_client(client):
    while True:
        try:
            username = client.recv(1024).decode("utf-8")
            print(f"{HOST}:",username)
            password = client.recv(1024).decode("utf-8")
            print(f"{HOST}:", password)
            password = hashlib.sha256(password).hexdigest()
            print(password)
            conn = sqlite3.connect("hello.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username,password))

            if cur.fetchall():
                client.send("200".encode("utf-8"))

            else:
                print("failed")
                remove_client(client)
            conn.close()
        except Exception as e:
            print(f"[ERROR] {e}")
            remove_client(client)
            break


def remove_client(client):
    if client in client_socket:
        client_socket.remove(client)


def start_server():
    print(f"Server is starting......\n[LISTENING] on {HOST}:{PORT}")
    threading.Thread(target=accept_client).start()


def accept_client():
    while True:
        client, address = s.accept()
        print(f"[NEW CONNECTION] {address}")
        client_socket.append(client)
        print(client_socket)
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    start_server()
