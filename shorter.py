import serial
import time
import numpy
from os import mkdir
import matplotlib.pyplot as plt

port = serial.Serial()
port.baudrate = 9600
port.port = "COM5"
port.timeout = 25

imageGroupCount = 45
newTempTag = 1
groupTempAverage = 0.0

def make_heatmap(heat_array):
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
      current_time = time.strftime("%H-%M-%S", time.localtime())
      heat_array_group = numpy.reshape([float(i) for i in arduino_message[:-1].split(" ")], (imageGroupCount, 64)) 
      
      group_temp_average = 0.0
     
      for i in heat_array_group:
        group_temp_average += i.max()
      
      group_temp_average /= imageGroupCount
      heat_array_group = sorted(heat_array_group, key=find_max_difference)[:15]
      group_folder = "C:/Users/smize1/Documents/({}) {:.2f}".format(current_time, group_temp_average)
      mkdir(group_folder)
   
      for i in heat_array_group:
        make_heatmap(i)
        plt.savefig(fname= group_folder + "/map" + str(i+1) + "(" + str(i.max()) + ").png", format="png")
    elif x == b'5':
      heat_array = make_heatmap([float(i) for i in arduino_message[:-1].split(" ")])
      plt.savefig(fname="C:/Users/smize1/Documents/Heatmap(" + str(heat_array.max()) + ").png", format="png") 
    else:
      print(arduino_message)
