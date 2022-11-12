import socket
import sys
import re
# TODO: talk 2 hemi


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


# bind a name to the program
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(sys.argv[1])))


# keep track of the users and the messages
users = {}
messages = []


# functionality
def join_chat(user_input, user_addr):
    name = re.search('1 (.*)', user_input)

    if not name:
        return -1

    if user_addr in users:
        return -1

    # add the user to the dictionary, and save a pointer to his first unread message
    users[user_addr] = (name.group(1), len(messages))
    messages.append(f'{name.group(1)} has joined')


def send_message(user_input, user_addr):
    if user_addr not in users:
        return -1

    message = re.search('2 (.*)', user_input)

    if not message:
        return -1

    messages.append(f'{users[user_addr][0]}: {message.group(1)}')


def change_name(user_input, user_addr):
    new_name = re.search('3 (.*)', user_input)

    if not new_name:
        return -1

    if user_addr not in users:
        return -1

    messages.append(f'{users[user_addr][0]} changed his name to {new_name.group(1)}')
    users[user_addr] = (new_name.group(1), users[user_addr][1])


def leave_group(user_input, user_addr):
    if len(user_input) > 1:
        return -1

    if user_addr not in users:
        return -1

    messages.append(f'{users[user_addr][0]} has left the group')
    users.pop(user_addr)


def read_messages(user_input, user_addr):
    if len(user_input) > 1:
        return -1

    if user_addr not in users:
        return -1

    if users[user_addr][1] == len(messages):
        return -1

    # tell the user how many messages to read, and send the unread messages to the user
    unread_messages = [messages[i] for i in range(users[user_addr][1], len(messages))]

    s.sendto(str(len(unread_messages)).encode(), user_addr)

    for message in unread_messages:
        s.sendto(message.encode(), user_addr)

    # update the user's first unread message
    users[user_addr] = (users[user_addr][0], len(messages))

    # delete unnecessary messages, and update all users' last unread message
    index = min([v[1] for v in users.values()])
    del messages[0: index]

    for k in users.keys():
        users[k] = (users[k][0], users[k][1] - index)


def parse_input(user_input, user_addr):
    # if no input was detected
    if len(user_input) == 0:
        s.sendto(b'0', user_addr) #TODO

    option = user_input[0]

    options = {'1': join_chat,
               '2': send_message,
               '3': change_name,
               '4': leave_group,
               '5': read_messages}

    if option in options:
        did_succeed = options[option](user_input, user_addr)

        if did_succeed == -1:
            s.sendto(b'1', user_addr)
            s.sendto(b'Illegal Request', user_addr)

        # TODO
        elif option in ['2', '3', '5']:
            read_messages('5', user_addr)

        else:
            s.sendto(b'0', user_addr)


while True:
    data, addr = s.recvfrom(1024)
    print(data.decode())
    parse_input(data.decode(), addr)
