from inputs import get_gamepad
import pyvjoy

# vjoy device to be fed data
j = pyvjoy.VJoyDevice(1)


# function to handle setting the button state
def setState(btn, state):
    j.set_button(btn, state)


# function to handle button mapping
def buttonState(eventCode, eventState):
    # A button
    if eventCode == "BTN_SOUTH":
        j.reset()
        if eventState == 1:
            setState(1, 1)
        else:
            setState(1, 0)
    # B button
    if eventCode == "BTN_EAST":
        if eventState == 1:
            setState(2, 1)
        else:
            setState(2, 0)
    # X button
    if eventCode == "BTN_WEST":
        if eventState == 1:
            setState(3, 1)
        else:
            setState(3, 0)
    # Y button
    if eventCode == "BTN_NORTH":
        if eventState == 1:
            setState(4, 1)
        else:
            setState(4, 0)
    # left bumper
    if eventCode == "BTN_TL":
        if eventState == 1:
            setState(5, 1)
        else:
            setState(5, 0)
    # right bumper
    if eventCode == "BTN_TR":
        if eventState == 1:
            setState(6, 1)
        else:
            setState(6, 0)
    # start button
    if eventCode == "BTN_START":
        if eventState == 1:
            setState(7, 1)
        else:
            setState(7, 0)
    # back button
    if eventCode == "BTN_SELECT":
        if eventState == 1:
            setState(8, 1)
        else:
            setState(8, 0)
    # left stick click
    if eventCode == "BTN_THUMBL":
        if eventState == 1:
            setState(9, 1)
        else:
            setState(9, 0)
    # right stick click
    if eventCode == "BTN_THUMBR":
        if eventState == 1:
            setState(10, 1)
        else:
            setState(10, 0)


# function to handle axis translation and position
def setAxis(state, XY):
    offset1 = (state + 32768) / 2
    offset2 = (state + 32768) / -2 + 32768
    # 0 for x axis
    if XY == 0:
        j.set_axis(pyvjoy.HID_USAGE_X, offset1)
    # 1 for y axis
    if XY == 1:
        j.set_axis(pyvjoy.HID_USAGE_Y, offset2)
    # 2 for rx axis
    if XY == 2:
        j.set_axis(pyvjoy.HID_USAGE_RX, offset1)
    # 3 for ry axis
    if XY == 3:
        j.set_axis(pyvjoy.HID_USAGE_RY, offset2)


# function to handle trigger values
def setTriggers(state, LR):
    # 0 for left trigger
    if LR == 0:
        j.set_axis(pyvjoy.HID_USAGE_Z, 25)
    # 1 for right trigger
    if LR == 1:
        j.set_axis(pyvjoy.HID_USAGE_RZ, 25)


def main():
    while True:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)
            # to handle button presses
            if event.code[:3] == "BTN":
                buttonState(event.code, event.state)
            # to handle left and right stick position
            if event.code == "ABS_X":
                setAxis(event.state, 0)
            if event.code == "ABS_Y":
                setAxis(event.state, 1)
            if event.code == "ABS_RX":
                setAxis(event.state, 2)
            if event.code == "ABS_RY":
                setAxis(event.state, 3)
            # to handle triggers
            # if event.code == "ABS_Z":
            #     setTriggers(event.state, 0)
            #     print(pyvjoy.HID_USAGE_Z)
            # if event.code == "ABS_RZ":
            #     setTriggers(event.state, 1)
            #     print(pyvjoy.HID_USAGE_RZ)
            # if event.code == "ABS_HAT0Y":
            #     print(event.ev_type, event.code, event.state)


if __name__ == '__main__':
    main()
