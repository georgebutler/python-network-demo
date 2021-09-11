import socket
import pickle
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 32007))
server.listen()

print("Server now listening for connections.")


def threaded_client(connection, address):
    print("New client connected: ", address)
    connection.send("Hello from server!".encode())


while True:
    conn, addr = server.accept()

    thread = threading.Thread(target=threaded_client, args=(conn, addr))
    thread.start()
