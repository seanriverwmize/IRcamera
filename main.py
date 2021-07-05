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
        arduino_message = arduino_message[:-1]
        heat_values = arduino_message.split(" ")
        #print(len(heat_values))
        heat_array = numpy.zeros((8, 8))
        for i in range(64):
          for j in range(8):
            for z in range(8):
              heat_array[j][z] = float(heat_values[i])
              #print(heat_values[i])
              i += 1
              z += 1
            z = 0  
            j += 1
          j = 0
          if(i == 64): break;
        print(heat_array)
          
        fig, ax = plt.subplots()
        im = ax.imshow(heat_array)
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Degrees Celcius", rotation=-90, va="bottom")
        for i in range(8):
          for j in range(8):
            text = ax.text(j, i, heat_array[i, j], ha="center", va="center", color="w")
        ax.set_title("Thermal Image")
        fig.tight_layout()
        plt.savefig(fname="C:/Users/smize1/Documents/Heatmap.png", format="png")
        plt.show()
    
