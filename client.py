import socket

'''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Hello world', ('127.0.0.1', 12345))

data, addr = s.recvfrom(1024)
print(str(data), addr)

s.close()
'''

lst = [1,2,3,4,5]

index = [i for i, v in enumerate(lst) if v == 19]

print(index)

