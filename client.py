import socket
import sys


# greet the user
print('    __  __               _ _          _       __     __       ________          __     _____  ____ \n'
      '   / / / /__  ____ ___  (_| )_____   | |     / /__  / /_     / ____/ /_  ____ _/ /_   / ___/ / __ \\\n'
      '  / /_/ / _ \\/ __ `__ \\/ /|// ___/   | | /| / / _ \\/ __ \\   / /   / __ \\/ __ `/ __/  / __ \\ / /_/ /\n'
      ' / __  /  __/ / / / / / /  (__  )    | |/ |/ /  __/ /_/ /  / /___/ / / / /_/ / /_   / /_/ / \\__, /\n'
      '/_/ /_/\\___/_/ /_/ /_/_/  /____/     |__/|__/\\___/_.___/   \\____/_/ /_/\\__,_/\\__/   \\____(_)____/\n')


# do other stuff
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

while True:
    message = input()
    s.sendto(message.encode(), (server_ip, server_port))

    data, addr = s.recvfrom(1024)

    for i in range(0, int(data.decode())):
        data, addr = s.recvfrom(1024)
        print(data.decode())
