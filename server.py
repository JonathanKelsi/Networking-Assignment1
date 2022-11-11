import socket
import sys
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

if sys.argv[1] == '--help':
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


# utility functions
def get_user_by_addr(user_addr):
    user_index = [i for i, u in enumerate(users) if u[1] == user_addr]

    if len(user_index) == 0:
        return None

    return user_index[0]


# functionality
def join_chat(user_input, user_addr):
    name = re.search('1 (.*)', user_input).group(1)

    if not name:
        return

    if get_user_by_addr(user_addr):
        return

    users.append((name, user_addr, 0))
    messages.append((name, f'{name} has joined'))


def send_message(user_input, user_addr):
    index = get_user_by_addr(user_addr)

    if not index:
        return

    message = re.search('2 (.*)', user_input).group(1)

    if not message:
        return

    messages.append((users[index][1], message))


def change_name(user_input, user_addr):
    new_name = re.search('3 (.*)', user_input).group(1)

    if not new_name:
        return

    index = get_user_by_addr(user_addr)

    if not index:
        return

    messages.append(f'{users[index][0]} changed his name to {new_name}')
    users[index][0] = new_name


def leave_group(user_input, user_addr):
    if len(user_input) > 1:
        return

    index = get_user_by_addr(user_addr)

    if not index:
        return

    messages.append(f'{users[index][0]} has left the group')
    del users[index]


def read_messages(user_input, user_addr):
    pass


def parse_input(user_input, user_addr):
    if len(user_input) == 0:
        return

    match user_input[0]:
        case '1':
            join_chat(user_input, user_addr)
        case '2':
            send_message(user_input, user_addr)
        case '3':
            change_name(user_input, user_addr)
        case '4':
            leave_group(user_input, user_addr)


while True:
    data, addr = s.recvfrom(1024)
    print(str(data), addr)
    s.sendto(data.upper(), addr)
