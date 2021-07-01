import serial
import PySimpleGUI as sg

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


port = serial.Serial(port = "COM9", baudrate = 9600, timeout = 0.1) #connect to Arduino Port
arduino_serial_data = port.readline().decode('utf-8') # Read and Translate Serial data 
print(arduino_serial_data)

while True:
    x = input("What would you like to send: ")
    # x = x + "\n"
    port.write(x)
    arduino_message = port.readline('utf-8')
    print(response)
    