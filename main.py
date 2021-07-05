import serial
import numpy
import matplotlib.pyplot as plt

port = serial.Serial(port = "COM7", baudrate = 9600, timeout = 4) #connect to Arduino Port
arduino_serial_data = port.readline().decode('utf-8') # Read and Translate Serial data 
print(arduino_serial_data)

imageGroupCount = 15
newTempTag = 1
groupTempAverage = 0.0

def make_heatmap():
    heat_array = arduino_message.split(" ")
    for i in range(len(heat_array)):
      heat_array[i] = float(heat_array[i])
    heat_array = numpy.reshape(heat_array, (8, 8))
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
    return heat_array
while True:
    x = input("What would you like to send: ").encode()
    port.write(x)
    arduino_message = port.read_until(expected="&".encode('utf-8')).decode('utf-8')
    arduino_message = arduino_message[:-1]
    if x == b'1':
      print(arduino_message)  
    elif x == b'5':
      arduino_message = arduino_message[:-1]
      heat_array = make_heatmap()
      print(heat_array.max())
      plt.savefig(fname="C:/Users/smize1/Documents/Heatmap.png", format="png") 
    else:
      print(arduino_message)
      print("maximus")
