import sys
import socket
import re

# check input validity
usage_instructions = 'Usage: python server.py [port]\n' \
                     'Try "python server.py --help" for more information.'

server_description = 'Start the web chat server\n' \
                     'NOTE: The port number must be an integer in the range 1024 - 65535.\n' \
                     'EXAMPLE: python server.py 42069'

if len(sys.argv) != 2:
    print(usage_instructions)
    exit(1)

if sys.argv[1] == "--help":
    print(server_description)
    exit(1)

if not (sys.argv[1].isnumeric() and int(sys.argv[1]) in range(1025, 2 ** 16)):
    print(usage_instructions)
    exit(1)

# greet the user
usr_msg = '    __  __               _ _          _       __     __       ________          __     _____  ____ \n' \
          '   / / / /__  ____ ___  (_| )_____   | |     / /__  / /_     / ____/ /_  ____ _/ /_   / ___/ / __ \\\n' \
          '  / /_/ / _ \\/ __ `__ \\/ /|// ___/   | | /| / / _ \\/ __ \\   / /   / __ \\/ __ `/ __/  / __ \\ / /_/ /\n' \
          ' / __  /  __/ / / / / / /  (__  )    | |/ |/ /  __/ /_/ /  / /___/ / / / /_/ / /_   / /_/ / \\__, /\n' \
          '/_/ /_/\\___/_/ /_/ /_/_/  /____/     |__/|__/\\___/_.___/   \\____/_/ /_/\\__,_/\\__/   \\____(_)____/\n'

print(usr_msg)

# bind a name to the program
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', int(sys.argv[1])))

# keep track of the users and the messages
users = []
messages = []


# functionality
def join(message, user_addr):
    name = re.search("1 .*", message)

    if not name:
        return

    users.insert((name, user_addr, 0))


def parse_input(message, user_addr):
    if len(message) == 0:
        return

    match message[0]:
        case '1':
            join(message, user_addr)


while True:
    data, addr = s.recvfrom(1024)
    print(str(data), addr)
    s.sendto(data.upper(), addr)
