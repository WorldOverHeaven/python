import os
import time

read = open('Cwrite', 'r')
write = open('Pwrite', 'w')


def put(a, i, j):
    write.write("put\n")
    write.write(str(a)+"\n")
    write.write(str(i)+"\n")
    write.write(str(j)+"\n")
    os.system(r'/home/kirill/CLionProjects/XO3/main.cpp')
    time.sleep(0.1)
    string = read.readline()
    i = read.readline()
    j = read.readline()
    arr = [string, i, j]
    return arr


def nextMove(a):
    write.write("nextMove\n")
    write.write(str(a) + "\n")
    os.system(r'/home/kirill/CLionProjects/XO3/main.cpp')
    time.sleep(0.1)
    i = read.readline()
    j = read.readline()
    arr = [i, j]
    return arr


nextMove(361*" ")

# import socket
#
# sock = socket.socket(
#     socket.AF_INET,
#     socket.SOCK_STREAM,
# )
#
# sock.bind(
#     ("", 9090)
# )
#
# sock.listen(1)
#
# conn, addr = sock.accept()
#
# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.send(data.upper())
