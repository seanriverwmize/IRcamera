import serial
import PySimpleGUI as sg
import numpy
import matplotlib.pyplot as plt
# layout = [
#     [sg.Text("Hey World"), sg.Text("00")],
#     [sg.Button("RUN COMMAND"), sg.Button("RUN COMMAND"), sg.Button("RUN COMMAND"), sg.Button("RUN COMMAND"), sg.Button("RUN COMMAND")]
# ]

# window = sg.Window("Window", layout, margins=(600,400))

# while True:
#     event, values = window.read()
#     if event == "RUN COMMAND" or event == sg.WIN_CLOSED:
#         break
# window.close()


port = serial.Serial(port = "COM5", baudrate = 9600, timeout = 4) #connect to Arduino Port
arduino_serial_data = port.readline().decode('utf-8') # Read and Translate Serial data 
print(arduino_serial_data)

while True:
    x = input("What would you like to send: ").encode()
    port.write(x)
    arduino_message = port.read_until(expected="&".encode('utf-8')).decode('utf-8')
    arduino_message = arduino_message[:-1]
    if x == b'5':
        print("Success")
        a = numpy.random.random((16,16))
        plt.imshow(a, cmap="hot", interpolation='nearest')
        plt.show()
    else:
        print(arduino_message)
    
