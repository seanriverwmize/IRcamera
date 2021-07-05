port = serial.Serial(port = "COM5", baudrate = 9600, timeout = 4) #connect to Arduino Port
arduino_serial_data = port.readline().decode('utf-8') # Read and Translate Serial data 
print(arduino_serial_data)

heat_array = numpy.zeros((8, 8))
imageGroupCount = 15
newTempCount = 1
groupTempAverage = 0.0

def make_heatmap():
    heat_values = arduino_message.split(" ")
    for i in range(64):
      for j in range(8):
        for z in range(8):
          heat_array[j][z] = float(heat_values[i])
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
while True:
    x = input("What would you like to send: ").encode()
    if x == b'1':
      port.write(b'3') #shutter opens
      for i in range(imageGroupCount):
        port.write(b'5') #captures image
        arduino_message = port.read_until(expected="&".encode('utf-8')).decode('utf-8')
        arduino_message = arduino_message[:-2]
        make_heatmap()
        groupTempAverage += heat_array.max
        map_file_name = "C:/Users/smize1/Documents/" + str(heat_array.max) + "Heatmap
        i += 1
    else:
      port.write(x)
      arduino_message = port.read_until(expected="&".encode('utf-8')).decode('utf-8')
      arduino_message = arduino_message[:-1]
      if x == b'5':
        arduino_message = arduino_message[:-1]
        make_heatmap()
        plt.savefig(fname="C:/Users/smize1/Documents/Heatmap.png", format="png")
        print(heat_array.max())
      else:
        print(arduino_message)
