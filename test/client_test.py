import socket

s = socket.socket()

port = 12244

s.connect(('127.0.0.1', port))

while True:
    s.send("from client".encode('ascii'))
    # data = s.recv(1024)
    # msg = data.decode('ascii')
    # print(msg + " --client side")
