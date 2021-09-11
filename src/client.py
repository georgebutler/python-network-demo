import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 32007))

message = client.recv(1024)
print(message.decode())
