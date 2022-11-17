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


# functionality
def join_chat(user_addr, name):
    if user_addr in users:
        return -1

    # add the user to the dictionary, and save a pointer to his first unread message
    users[user_addr] = (name, len(messages))
    messages.append(f'{name} has joined')


def send_message(user_addr, message):
    if user_addr not in users:
        return -1

    messages.append(f'{users[user_addr][0]}: {message.group(1)}')


def change_name(user_addr, new_name):
    if user_addr not in users:
        return -1

    messages.append(f'{users[user_addr][0]} changed his name to {new_name.group(1)}')
    users[user_addr] = (new_name.group(1), users[user_addr][1])


def leave_group(user_addr):
    if user_addr not in users:
        return -1

    messages.append(f'{users[user_addr][0]} has left the group')
    users.pop(user_addr)


def read_messages(user_addr):
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


def send_error_message(user_addr):
    s.sendto(b'1', user_addr)
    s.sendto(b'Illegal Request', user_addr)


def parse_input(user_input, user_addr):
    # check for format validity
    input_type1 = re.search("([1-3]) (.+)", user_input)
    input_type2 = re.search("([4-5])", user_input)

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
        did_succeed = options[option](user_addr, content)

    elif input_type2 is not None:
        option = input_type2.group(1)
        did_succeed = options[option](user_addr)

    if did_succeed == -1:
        send_error_message(user_addr)

    elif option in ['2', '3']:
        read_messages(user_addr)


while True:
    data, addr = s.recvfrom(1024)
    print(data.decode())
    parse_input(data.decode(), addr)
