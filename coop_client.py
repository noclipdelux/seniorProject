from inputs import get_gamepad
import socket


# client class to handle connection
class Client:
    def __init__(self, address, port):
        self.port = port
        self.address = address
        self.sock = socket.socket()

    # connects to server
    def connect(self):
        try:
            self.sock.connect((self.address, self.port))
        except socket.error:
            print("Connection failed, shutting down")
            self.closeConnection()
            exit(1)
        print("Connection established to: " + str(self.address))

    # closes connection
    def closeConnection(self):
        self.sock.close()

    # send data
    def send(self, msg):
        encoded = msg.encode('ascii')
        self.sock.send(encoded)


# disconnects on left trigger
def checkDisconnect(client, code):
    if code == "ABS_Z":
        client.closeConnection()
        print("Trigger detected, shutting down")
        exit(0)

def main():
    c = Client('127.0.0.1', 12244)
    c.connect()

    while True:
        # gets all events for controller
        events = get_gamepad()
        # send all events in list
        for event in events:
            code = str(event.code)
            state = str(event.state)
            checkDisconnect(c, code)
            c.send(code + ',' + state)


main()
