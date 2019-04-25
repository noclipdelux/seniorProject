import socket
import pyvjoy


# server class to handle connection
class Server:
    def __init__(self, port):
        self.port = port
        self.address = ''
        self.sock = socket.socket()
        self.connection, self.clientAddress = self.listen()

    # binds server to socket
    def bindServer(self):
        self.sock.bind((self.address, self.port))
        print("Server bound to port %d" % self.port)

    # listens on port for incoming connections
    # returns connection object, client address
    def listen(self):
        self.bindServer()
        self.sock.listen(5)
        print("Waiting for connections...")
        connection = ''
        address = ''
        try:
            connection, address = self.sock.accept()
        except socket.error:
            print("Connection failed, shutting down")
            self.closeConnection()
            exit(1)
        print("Connection established to: " + str(address))
        return connection, address

    # closes connection
    def closeConnection(self):
        self.sock.close()

    # receives data from client
    # returns ascii message
    def receive(self):
        data = self.connection.recv(1024)
        msg = data.decode('ascii')
        return msg


# feeder class to handle data formatting and usage
class Feeder:
    def __init__(self):
        self.dev = pyvjoy.VJoyDevice(1)

    # feeds data to appropriate buttons/triggers
    def feed(self, data):
        event, code = self.format(data)
        # TODO: create handler methods and split control flow here
        return

    # formats incoming data stream - static, does not alter instance variables
    @staticmethod
    def format(data):
        dataSplit = data.split(',')
        event = dataSplit[0]
        code = dataSplit[1]
        return event, code


# checks data stream for empty strings
def checkStream(server, data):
    if data == '':
        server.closeConnection()
        print("Getting empty strings, shutting down")
        exit(0)


def main():
    s = Server(12244)
    f = Feeder

    while True:
        data = s.receive()
        checkStream(s, data)


main()
