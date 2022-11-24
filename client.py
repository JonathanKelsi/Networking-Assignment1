import socket
import sys


# utility function
def validate_ip(address):
    try:
        socket.inet_aton(address)
        return True

    except socket.error:
        return False


# check input validity
usage_instructions = 'Usage: python client.py [ip] [port]\n' \
                     'Try "python client.py --help" for more information.'

server_description = 'Start the web chat client\n' \
                     'NOTE: The port number must be an integer in the range 1024 - 65535.\n' \
                     'In addition, the ip must be in the form [0-255].[0-255].[0-255].[0-255].\n' \
                     'EXAMPLE: python client.py 127.0.0.1 42069'

if len(sys.argv) == 2 and sys.argv[1] == '--help':
    print(server_description)
    exit(1)

if len(sys.argv) != 3:
    print(usage_instructions)
    exit(1)

if not (sys.argv[2].isnumeric() and int(sys.argv[2]) in range(1025, 2 ** 16 - 1) and validate_ip(sys.argv[1])):
    print(usage_instructions)
    exit(1)

# connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

# communicate with the server
while True:
    message = input()
    s.sendto(message.encode(), (server_ip, server_port))

    data, addr = s.recvfrom(1024)

    for i in range(0, int(data.decode())):
        data, addr = s.recvfrom(1024)
        print(data.decode())
