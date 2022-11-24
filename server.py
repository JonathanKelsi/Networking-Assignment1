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

if not (sys.argv[1].isnumeric() and int(sys.argv[1]) in range(1025, 2 ** 16 - 1)):
    print(usage_instructions)
    exit(1)


# bind a name to the program
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', int(sys.argv[1])))


# keep track of the users and the messages
users = {}
messages = []


# utility functions for communication with client
def send_data(user_addr, n, lst):
    s.sendto(str(n).encode(), user_addr)

    for m in lst:
        s.sendto(m.encode(), user_addr)


def send_error_message(user_addr):
    send_data(user_addr, 1, ['Illegal Request'])


def skip_recv(user_addr):
    send_data(user_addr, 0, [])


# functionality
def join_chat(user_addr, name):
    if user_addr in users:
        send_error_message(user_addr)
        return

    # send the current users
    if len(users) != 0:
        send_data(user_addr, 1, [(', '.join([u[0] for u in users.values()][::-1]))])

    else:
        skip_recv(user_addr)

    # add the user to the dictionary, and save a pointer to his first unread message
    users[user_addr] = (name, len(messages) + 1)
    messages.append((user_addr, name + ' has joined'))


def send_message(user_addr, message):
    if user_addr not in users:
        send_error_message(user_addr)
        return

    messages.append((user_addr, users[user_addr][0] + ': ' + message))


def change_name(user_addr, new_name):
    if user_addr not in users:
        send_error_message(user_addr)
        return

    messages.append((user_addr, users[user_addr][0] + ' has changed his name to ' + new_name))
    users[user_addr] = (new_name, users[user_addr][1])


def leave_group(user_addr):
    if user_addr not in users:
        send_error_message(user_addr)
        return

    messages.append((user_addr, users[user_addr][0] + ' has left the group'))
    users.pop(user_addr)
    skip_recv(user_addr)


def read_messages(user_addr):
    if user_addr not in users:
        send_error_message(user_addr)
        return

    if users[user_addr][1] == len(messages):
        skip_recv(user_addr)
        return

    # tell the user how many messages to read, and send the unread messages to the user
    unread_messages = [messages[i][1] for i in range(users[user_addr][1], len(messages)) if messages[i][0] != user_addr]

    send_data(user_addr, len(unread_messages), unread_messages)

    # update the user's first unread message
    users[user_addr] = (users[user_addr][0], len(messages))

    # delete unnecessary messages, and update all users' last unread message
    index = min([v[1] for v in users.values()])
    del messages[0: index]

    for k in users.keys():
        users[k] = (users[k][0], users[k][1] - index)


def parse_input(user_input, user_addr):
    # check for format validity
    input_type1 = re.search("^([1-3]) (.+)", user_input)
    input_type2 = re.search("^([4-5])$", user_input)

    if not input_type1 and not input_type2:
        send_error_message(user_addr)
        return

    # handle the request
    options = {'1': join_chat,
               '2': send_message,
               '3': change_name,
               '4': leave_group,
               '5': read_messages}

    if input_type1 is not None:
        option, content = input_type1.group(1), input_type1.group(2)
        options[option](user_addr, content)

    elif input_type2 is not None:
        option = input_type2.group(1)
        options[option](user_addr)

    if option in ['2', '3']:
        read_messages(user_addr)


# communicate with clients
while True:
    data, addr = s.recvfrom(1024)
    parse_input(data.decode(), addr)
