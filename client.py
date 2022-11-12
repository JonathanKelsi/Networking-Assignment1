import socket



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# s.sendto(b'Hello world', ('127.0.0.1', 12345))

server_ip = '127.0.0.1'
server_port = 12345

# def register(name):
#     full_output = f'1 {name}'
#     s.sendto(full_output.encode('ascii') , (server_ip, server_port))
#
# def send_message(message):
#     full_output = f'2 {message}'
#     s.sendto(full_output.encode('ascii') , (server_ip, server_port))


def run_option(option):
    full_message = ''
    match option:
        case '1':
            name = input("Enter a name:")
            full_message += f'1 {name}'
        case '2':
            message = input("Enter a message:")
            full_message += f'2 {message}'
        case '3':
            name = input("Enter a new name:")
            full_message += f'3 {name}'
        case '4':
            full_message += '4'
        case '5':
            full_message += '5'

    s.sendto(full_message.encode('ascii') , (server_ip, server_port))


data, addr = s.recvfrom(1024)
print(str(data), addr)

s.close()


