import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = '127.0.0.1'
server_port = 12345
default_buffer_size = 1024

while True:
    message = input()
    s.sendto(message.encode('ascii') , (server_ip, server_port))
    data, addr = s.recvfrom(default_buffer_size)
    print(data)

s.close()