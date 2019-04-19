from inputs import get_gamepad
import socket

s = socket.socket()
port = 12244
ip = ''
s.bind((ip, port))
s.listen(1)
c, address = s.accept()

while True:
    data = c.recv(1024)
    print(data)
    events = get_gamepad()
    for event in events:
        msg = event.ev_type, event.code, event.state
        strMsg = str(msg)
        c.send(strMsg.encode('ascii'))
