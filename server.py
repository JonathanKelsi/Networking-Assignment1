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
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(sys.argv[1])))


# keep track of the users and the messages
users = {}
messages = []


# functionality
def join_chat(user_input, user_addr):
    name = re.search('1 (.*)', user_input).group(1)

    if not name:
        return

    if user_addr in users:
        return

    # add the user to the dictionary, and save a pointer to his first unread message
    users[user_addr] = (name, 0)
    messages.append(f'{name} has joined')


def send_message(user_input, user_addr):
    if user_addr not in users:
        return

    message = re.search('2 (.*)', user_input).group(1)

    if not message:
        return

    messages.append(f'{users[user_addr][0]}: {message}')


def change_name(user_input, user_addr):
    new_name = re.search('3 (.*)', user_input).group(1)

    if not new_name:
        return

    if user_addr not in users:
        return

    messages.append(f'{users[user_addr][0]} changed his name to {new_name}')
    users[user_addr][0] = new_name


def leave_group(user_input, user_addr):
    if len(user_input) > 1:
        return

    if user_addr not in users:
        return

    messages.append(f'{users[user_addr][0]} has left the group')
    users.pop(user_addr)


def read_messages(user_input, user_addr):
    if user_addr not in users:
        return

    if users[user_addr][1] == len(messages):
        return

    # send the unread messages to the user
    unread_messages = [messages[i] for i in range(users[user_addr][1], len(messages))]

    for message in unread_messages:
        s.sendto(message, user_addr)

    # update the user's first unread message
    users[user_addr][1] = len(messages)

    # delete unnecessary messages, and update all users' unread messages count
    index = min([v[1] for k, v in users])
    del messages[0: index + 1]

    for k, v in users:
        v[1] -= index



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
