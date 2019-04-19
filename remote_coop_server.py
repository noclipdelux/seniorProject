import socket
import pyvjoy


# server class to handle data
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
        connection, address = self.sock.accept()
        if connection == '' or address == '':
            print("Connection failed, shutting down")
            self.closeConnection()
            exit(1)
        else:
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

    # sends data
    def send(self, msg):
        encoded = msg.encoded('ascii')
        self.connection.send(encoded)


def main():
    s = Server(12244)

    while True:
        print(s.receive())


main()
