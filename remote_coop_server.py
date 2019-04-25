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
        # grabs first joystick device (should be xbox one controller)
        self.dev = pyvjoy.VJoyDevice(1)
        self.isFeeding = False

    # feeds data to appropriate buttons/triggers
    def feed(self, data):
        self.isFeeding = True
        code, state = self.format(data)
        state = int(state)
        # handles button presses
        if code[:3] == "BTN":
            self.setButton(code, state)
        # next two handle left stick
        if code == "ABS_X":
            self.setAxis(state, 0)
        if code == "ABS_Y":
            self.setAxis(state, 1)
        # last two handle right stick
        if code == "ABS_RX":
            self.setAxis(state, 2)
        if code == "ABS_RY":
            self.setAxis(state, 3)
        return code

    # handles button presses and sends to virtual controller
    def setButton(self, code, state):
        # A button
        if code == "BTN_SOUTH":
            if state == 1:
                self.dev.set_button(1, 1)
            else:
                self.dev.set_button(1, 0)
        # B button
        if code == "BTN_EAST":
            if state == 1:
                self.dev.set_button(2, 1)
            else:
                self.dev.set_button(2, 0)
        # X button
        if code == "BTN_WEST":
            if state == 1:
                self.dev.set_button(3, 1)
            else:
                self.dev.set_button(3, 0)
        # Y button
        if code == "BTN_NORTH":
            if state == 1:
                self.dev.set_button(4, 1)
            else:
                self.dev.set_button(4, 0)
        # left bumper
        if code == "BTN_TL":
            if state == 1:
                self.dev.set_button(5, 1)
            else:
                self.dev.set_button(5, 0)
        # right bumper
        if code == "BTN_TR":
            if state == 1:
                self.dev.set_button(6, 1)
            else:
                self.dev.set_button(6, 0)
        # start button
        if code == "BTN_START":
            if state == 1:
                self.dev.set_button(7, 1)
            else:
                self.dev.set_button(7, 0)
        # back button
        if code == "BTN_SELECT":
            if state == 1:
                self.dev.set_button(8, 1)
            else:
                self.dev.set_button(8, 0)
        # left stick click
        if code == "BTN_THUMBL":
            if state == 1:
                self.dev.set_button(9, 1)
            else:
                self.dev.set_button(9, 0)
        # right stick click
        if code == "BTN_THUMBR":
            if state == 1:
                self.dev.set_button(10, 1)
            else:
                self.dev.set_button(10, 0)

    # handles axis translation and position and sends to driver
    def setAxis(self, state, xy):
        offset1 = (state + 32768) / 2
        offset2 = (state + 32768) / -2 + 32768
        # 0 for x axis
        if xy == 0:
            self.dev.set_axis(pyvjoy.HID_USAGE_X, offset1)
        # 1 for y axis
        if xy == 1:
            self.dev.set_axis(pyvjoy.HID_USAGE_Y, offset2)
        # 2 for rx axis
        if xy == 2:
            self.dev.set_axis(pyvjoy.HID_USAGE_RX, offset1)
        # 3 for ry axis
        if xy == 3:
            self.dev.set_axis(pyvjoy.HID_USAGE_RY, offset2)

    # formats incoming data stream - static, does not alter instance variables
    @staticmethod
    def format(data):
        dataSplit = data.split(',')
        code = dataSplit[0]
        state = dataSplit[1]
        # sometimes the client concatenates state values to the code value
        # breaking the conversion from strings to ints
        # this will get rid of any code values in the state
        if len(state) > 6:
            state = state.split("ABS")[0]
        return code, state


# checks data stream for empty strings
def checkStream(server, data):
    if data == '':
        server.closeConnection()
        print("Getting empty strings, shutting down")
        exit(0)


def main():
    s = Server(12244)
    f = Feeder()

    while True:
        data = s.receive()
        checkStream(s, data)
        f.feed(data)
        # print(f.format(data))


main()
