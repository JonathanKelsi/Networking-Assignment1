import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
default_buffer_size = 1024

while True:
    message = input()
    s.sendto(message.encode('utf-8'), (server_ip, server_port))

    data, addr = s.recvfrom(default_buffer_size)
    print(data)

s.close()
