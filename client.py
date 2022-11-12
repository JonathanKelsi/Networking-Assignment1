import socket
import sys

# greet the user
usr_msg = '    __  __               _ _          _       __     __       ________          __     _____  ____ \n' \
          '   / / / /__  ____ ___  (_| )_____   | |     / /__  / /_     / ____/ /_  ____ _/ /_   / ___/ / __ \\\n' \
          '  / /_/ / _ \\/ __ `__ \\/ /|// ___/   | | /| / / _ \\/ __ \\   / /   / __ \\/ __ `/ __/  / __ \\ / /_/ /\n'\
          ' / __  /  __/ / / / / / /  (__  )    | |/ |/ /  __/ /_/ /  / /___/ / / / /_/ / /_   / /_/ / \\__, /\n' \
          '/_/ /_/\\___/_/ /_/ /_/_/  /____/     |__/|__/\\___/_.___/   \\____/_/ /_/\\__,_/\\__/   \\____(_)____/\n'

print(usr_msg)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
default_buffer_size = 1024

while True:
    message = input()
    s.sendto(message.encode('ascii') , (server_ip, server_port))
    data, addr = s.recvfrom(default_buffer_size)
    for i in range(0, int(data)):
        data, addr = s.recvfrom(default_buffer_size)
        print(data)