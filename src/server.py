import socket
import threading

server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
clients = []


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)
    threading._start_new_thread(accept_clients, (server, " "))


def accept_clients(the_server):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        threading._start_new_thread(display_client_info, (client, addr))


def display_client_info(client, addr):
    print("Client: %s, Address: %s", client, addr)


def main():
    start_server()


if __name__ == "__main__":
    main()
