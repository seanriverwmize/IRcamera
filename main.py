import serial
import time
import numpy
import matplotlib.pyplot as plt

port = serial.Serial()
port.baudrate = 9600
port.port = "COM6"
port.timeout = 10
#port = serial.Serial(port = "COM6", baudrate = 9600, timeout = 10) #connect to Arduino Port

imageGroupCount = 15
newTempTag = 1
groupTempAverage = 0.0

def make_heatmap(array):
    heat_array = array
    heat_array = numpy.reshape(heat_array, (8, 8))
    #print(heat_array)    
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

def find_max_difference(x):
    return abs(x.max() - group_temp_average)
while True:
    x = input("What would you like to send: ").encode()
    port.open()
    port.write(x)
    arduino_message = port.read_until(expected="&".encode('utf-8')).decode('utf-8')
    port.close()
    arduino_message = arduino_message[:-1]
    if x == b'1':
      arduino_message = arduino_message[:-1]
      heat_array_group = arduino_message.split(" ")
      for i in range(len(heat_array_group)):
        heat_array_group[i] = float(heat_array_group[i])
      heat_array_group = numpy.reshape(heat_array_group, (15, 64))
      group_temp_average = 0.0
      for i in range(15):
        group_temp_average += heat_array_group[i].max()
        #print(heat_array_group[i])
      group_temp_average /= 15
      #print(group_temp_average)
      heat_array_group = sorted(heat_array_group, key=find_max_difference)
      heat_array_group = heat_array_group[:5]
      #for i in range(len(heat_array_group)):
        #print(heat_array_group[i].max())
      for i in range(len(heat_array_group)):
        make_heatmap(heat_array_group[i])
        plt.savefig(fname="C:/Users/smize1/Documents/" + str(group_temp_average) + "/Heatmap" + str(i+1) + "(" + str(heat_array_group[i].max()) + ").png", format="png")
    elif x == b'5':
      arduino_message = arduino_message[:-1]
      heat_array_single = arduino_message.split(" ")
      for i in range(64):
        heat_array_single[i] = float(heat_array_single[i])
      heat_array = make_heatmap(heat_array_single)
      #print(heat_array.max())
      plt.savefig(fname="C:/Users/smize1/Documents/Heatmap(" + str(heat_array.max()) + ").png", format="png") 
    else:
      print(arduino_message)
