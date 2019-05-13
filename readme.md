Senior Project Documentation

Vasil Markov, Spring 2019

Project Objective
Create a system of remote connection using emulated drivers on a remote host. Connection is established to remote machine and input is streamed over the network in order to interact with host machine. A driver related to the input device is instantiated and data is fed to it through a socket. The screen is streamed over the network back to the user. The end goal is to be able to emulate a controller on remote host in order to participate in local coop games. 


Project repository: https://github.com/noclipdelux/seniorProject

General Information 

Windows Human Interface Devices (HID):

Windows HID is a generic USB driver for a variety of standard interfacing devices. In most cases, these devices include things like mice, keyboards, and game controllers. Before the HID protocol, most devices needed special drivers in order to work. Many vendors today use HID for proprietary drivers. Vendor specific USB protocols can also be used as 3rd party drivers. This project uses HID to gather the necessary input and stream it. 


HID is composed of two primary components. The Report Descriptor provides metadata about the report in use. Reports are the actual globs of data provided from the device. The current implementation uses Python and the inputs/winusb libraries to retrieve this information. Each HID provides a set number of capabilities (caps). In the case of controllers, these caps include axis control and button states. 


More information can found here: https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/

Virtual Drivers:

In the current implementation of the project, the remote machine uses a virtual driver known as VJoy. Vjoy creates a virtual controller driver that can be fed data through python and the pyvjoy package. The virtual controller can be configured to match the controller providing the data. In this case, the controller providing the data is an Xbox One controller. In device manager, the driver will show up as “vjoy device” and can be used as a controller. 


More information can found here:
http://vjoystick.sourceforge.net/site/index.php/dev216/system-architecture

DirectInput vs. XInput:

DirectInput and XInput provide an API for interfacing with Xbox 360/One controllers. DirectInput is the older implementation and is being replaced by XInput. DirectInput provides support for older controllers, but lacks many features and ease of use provided by the new XInput API. 


XInput is the new recommended method of interfacing with Xbox controllers. XInput requires less overhead and is easier to use. It also provides access to things like controller rumble and cross-platform programming. Both of these APIs work on top of the DirectX SDK, so an updated version of DirectX is required. DirectX is also required for some other parts of this project, so it’s important to have that installed. 


These APIs are important because they determine how values are being given and how values should be fed to the virtual controller. From the testing done on the virtual driver, it seems that it is working with XInput. However, depending on your controller the data may come through as DirectInput. There is a slight difference in trigger and stick values when comparing these two APIs. The trigger values are combined to one axis for DirectInput, while they are separate values on XInput. Axis values are on range of -32,000 to 32,000 on DirectInput and 0 to 32,000 on XInput. This has to be taken into account when writing your feeder application.


A detailed explanation on the use and differences of these APIs can be found here:
https://docs.microsoft.com/en-us/windows/desktop/xinput/xinput-and-directinput


Technology

Python

The project was primarily developed on Python 2.7 due to some of the packages being supported on older versions. However, when running into some interpreter issues, I also tried the project in 3.6 as well. This lead to some odd conversion errors when feeding data to the virtual driver, but alleviated other unrelated issues. 


My recommendation is to create two separate python interpreters in your development environment. One running 2.7 and one running 3.6. Make sure that the packages are installed the same way on both environments. Use the 2.7 version by default, but if you encounter any errors with not being able to read devices or pyvjoy not being able to find necessary files, run it with 3.6. 


Python downloads:
https://www.python.org/download/releases/2.7/
https://www.python.org/downloads/release/python-360/


Pointy’s Joystick Test

This small application is included in the git repository and is extremely useful when configuring and testing both the actual controller and the virtual one. In order to have it working properly you have to install DirectX version 9 and up. The easiest way to do this is to find the installer on the official Microsoft support website if the machine is new. If you are developing on a machine that has had previous game installed, odds are DirectX is already installed on it. 


Connect the controller and run an instance of the application to see the way it is configured. Once VJoy is installed, you can run a second instance of the application in order to configure the virtual controller. 

VJoy

In order to create a virtual controller you must download VJoy from their official website. Download and install the complete VJoy package. This will include utilities for testing and configuring the virtual device. Once installed, use Pointy’s Joystick Test to configure the virtual device to match the hardware controller you are using. If installed correctly, there should be an application called “Configure VJoy”. Run it and select the proper number of buttons, hats, axis, and triggers. The configuration app is fairly straightforward to use, you select the current default device and change the values. The driver will disconnect and reconnect with the proper configuration.


A warning on VJoy: If you have a physical controller connected and install VJoy, it will reinstall the drivers of that hardware controller. I am not sure why this happens, but you simply have to go to device manager (search device manager in windows) and under Human Interface Devices find the appropriate game controller and update the drivers (right click, update driver). This will put the physical controller back to its proper driver. In my development environment this made the Xbox controller run on DirectInput and the VJoy driver run on XInput. 


Download VJoy here:
http://vjoystick.sourceforge.net/site/index.php/download-a-install/download

Packages

When configuring your Python interpreter, be sure to install the following packages:
1. Inputs - access to hardware data streams
2. PyVJoy - wrapper for VJoy that allows you to feed data to the virtual driver
3. WinUsb - useful when debugging hardware issues, check the samples folder for scripts that retrieve hardware metadata 

Project Structure

Samples

Directory full of sample scripts from winusb that give information on hardware configuration
* rawData.py - get data on current HID devices plugged in, uses raw data
* showHID.py - prints a large list of HID devices and their metadata
* simpleFeature.py - finds device usage based on specified vendor and usage ID, change these IDs to the ones you need for your device
* simpleSend.py - attempts to send a click event to a specified device, use the vendor ID to specify which device you want

Test

Directory for all my initial test files before the code was refactored into objects
* client_test.py - a simple network client to receive data
* input_test.py - the primary file I worked with for testing
* server_test.py - the first iteration of the hosting server

Remaining Files

The files outside of the two previous directories
* coop_client.py - refactored object based code for the client side
* remote_coop_server.py - refactored object based code for the server side of the project
* HID.txt - a text dump from my systems HID for debugging
* JoystickTest.exe - test app mentioned in the section above

Install Process

Here is a basic rundown of the install process. Assuming you are installing on a fresh machine, this should get you to a running set up.


1. Install your IDE, I use Pycharm community for development
   1. https://www.jetbrains.com/pycharm/download/#section=windows
1. Install Python 2.7 and 3.6, add python to your PATH (part of the installer)
   1. https://www.python.org/download/releases/2.7/
   2. https://www.python.org/downloads/release/python-360/
1. Before cloning the repository, create your project interpreters in Pycharm, many guides exist for this
   1. https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html
   2. Install the packages mentioned before on both interpreters, test locally before testing over the network
1. Download and install VJoy for windows, see above sections for more details
   1. http://vjoystick.sourceforge.net/site/index.php/download-a-install/download
   2. Configure your virtual device following the steps mentioned before
   3. Have physical controller plugged in while doing this
1. Clone the github repository
   1. This can be done through Pycharm or through the git client
   2. https://github.com/noclipdelux/seniorProject
1. Before running any of the python files, be sure to open device manager and update the controller drivers
   1. Search “device manager” in start menu 
   2. Under “Human Interface Devices” find game controllers and update all of them
1. I would recommend running the input_test.py file first without dealing with networking
   1. Run with 2.7 interpreter 
   2. Test to see if you are getting any printed output from your controller
1. Run the client and server files
   1. Run the server file first
   2. Run the client file second
   3. Have two instances of the joystick test up to check to see if the physical controller input is being fed to the virtual controller
   4. By default the IP to connect to is localhost on port 12244
