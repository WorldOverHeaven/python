import os
import time
import subprocess

write = open('Pwrite', 'w')


def put(a, i, j):
    write.write("put\n")
    write.write(str(a) + "\n")
    write.write(str(i) + "\n")
    write.write(str(j) + "\n")
    subprocess.call("/home/kirill/CLionProjects/XO4/cmake-build-debug/XO4")
    read = open('Cwrite', 'r')
    string = read.readline()
    status = read.readline()
    arr = [string, status]
    # if len(arr) == 0:
    #     return put(a, i, j)
    print(arr)
    return arr


def nextMove(a):
    write.write("nextMove\n")
    write.write(str(a) + "\n")
    subprocess.call("/home/kirill/CLionProjects/XO4/cmake-build-debug/XO4")
    read = open('Cwrite', 'r')
    arr = read.readline()
    arr = arr.split()
    if len(arr) == 0:
        return nextMove(a)
    print(arr)
    return arr


def listen_put(a, b):
    inp = b"0 "
    for i in range(361):
        if a[i] == '0':
            inp += b"-1 "
        if a[i] == 'X':
            inp += b"1 "
        if a[i] == ' ':
            inp += b"0 "
    inp += str.encode(b)
    print(inp)
    args = ["/home/kirill/CLionProjects/XO4/cmake-build-debug/XO4"]
    result = subprocess.run(args, stdout=subprocess.PIPE, input=inp, shell=True, stderr=subprocess.STDOUT)
    s = result.stdout.decode('utf-8')
    s = s.split()
    ss = ""
    for i in range(361):
        if s[i] == '-1':
            ss += "0"
        if s[i] == '1':
            ss += "X"
        if s[i] == '0':
            ss += " "
    print(s)
    print(ss)
    arr = [ss, s[362]]
    return arr


def listen_next_move(a):
    inp = b"0 "
    for i in range(361):
        if a[i] == '0':
            inp += b"-1 "
        if a[i] == 'X':
            inp += b"1 "
        if a[i] == ' ':
            inp += b"0 "
    args = ["/home/kirill/CLionProjects/XO4/cmake-build-debug/XO4"]
    result = subprocess.run(args, stdout=subprocess.PIPE, input=inp, shell=True, stderr=subprocess.STDOUT)
    s = result.stdout.decode('utf-8')
    print(s)
    return listen_put(a, s)


listen_put(" X" + 360 * " ", "0 0")

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
