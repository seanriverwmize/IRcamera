//Include Libraries:
//Arduino SAMD Boards; Adafruit SAMD Board; Adafruit AMG88xx; TemperatureZero
#include <Wire.h>
#include <Adafruit_AMG88xx.h>
#include <Stepper.h>
#include <TemperatureZero.h>

int command; // Commands are read throught the Serial port as integers

Adafruit_AMG88xx amg;
float pixels[AMG88xx_PIXEL_ARRAY_SIZE];
const int minimum = 200; //Minimum Analog reading to read "Shutter is Open"
bool status;
const int imageGroupCount = 15;
float imagesArray[imageGroupCount*AMG88xx_PIXEL_ARRAY_SIZE];
const int totalSteps = 200; // Total number of steps per rotation of shutter motor
TemperatureZero TempZero = TemperatureZero();
float itsyBitsyTemperature;

//Stepper stepper(totalSteps, 12, 11, 9, 7); // Team 7 Pins used in order: AIN1, AIN2, BIN2, BIN1
Stepper stepper(totalSteps, 7, 9, 10, 11); //FLATSAT PINS order: AIN1, AIN2, BIN2, BIN1

void setup(void) {
  // Setup function needs to run once when instrument is plugged in
  Serial.begin(9600);
  status = amg.begin();
  if (!status) {
      Serial.println("Could not find a valid AMG88xx sensor, check wiring!");
      while (1);
  }
  pinMode(5, OUTPUT);
  //pinMode(A0, INPUT);
  stepper.setSpeed(60); // set the speed of the motor to 30 RPMs
  TempZero.init();
}

void captureImageGroup(){
  for(int i=1; i<= imageGroupCount; i++){  
    amg.begin();
    delay(120);
    amg.readPixels(pixels);
    for(int j=1; j<=AMG88xx_PIXEL_ARRAY_SIZE; j++){
        imagesArray[(64*(i-1))+(j-1)] = pixels[j-1];
        Serial.print(pixels[j-1]);
        Serial.print(" ");
    }
  }
  //Serial.print(imagesArray);
}

bool shutterStatus() { // "minimum" parameter is minumum analog reading when shutter is open
  // int photocellPin = A0;              // TEAM 7 photocell
  int photocellPin = 1;            // FLATSAT photocell
  int photocellAnalogReading;     // the analog reading from the voltage divider
            
  photocellAnalogReading = analogRead(photocellPin); //analogRead converts Voltage value to an integer 0 - 1023 
  //Serial.print("Photocell Reading: ");  
  //Serial.print(photocellAnalogReading);  // the raw analog reading prints to Serial
  //Serial.println("/1023");  
  if (photocellAnalogReading >= minimum){
  //Serial.println("Shutter is Open");
  return true;
  } else {
  //Serial.println("Shutter is Closed");
  return false;
  }
}

void shutterOpen(){   // parameter = number of 1/200 rotations motor will make if shutter is closed. param should be replaced with concrete value after testing
  if (shutterStatus() == false){// If shutter is closed, rotate motor. Otherwise, end function.
    stepper.step(170);   // rotate to shutter opening + a little extra for maximum FOV and internal light level
  }
    
}

void shutterClose(){
  while (shutterStatus() == true){
    stepper.step(1); // move 1.8 degrees until photocell detects no light
  }
}

void captureImage(){
  amg.begin();
  delay(120);
  amg.readPixels(pixels);
  for(int i=1; i<=AMG88xx_PIXEL_ARRAY_SIZE; i++){
    Serial.print(pixels[i-1]);
    Serial.print(" ");
  }
//    Serial.print(pixels[i-1]);
//    if(i == AMG88xx_PIXEL_ARRAY_SIZE){
//      Serial.print("]");
//    } else if( i%8 == 0 ){
//      Serial.println("],");
//      Serial.print("[");
//    } else Serial.print(", ");
//    }
//Serial.println("]");
//Serial.println();
}

void showInternalTemp(){
  itsyBitsyTemperature = TempZero.readInternalTemperature();
  Serial.print("Itsy Bitsy M4 Internal Temp: ");
  Serial.print(itsyBitsyTemperature);
  Serial.println(" degrees C");
  Serial.print("AMG8833 Internal Temp: ");
  Serial.print(amg.readThermistor());
  Serial.println(" degrees C");
}

void triggerEndRead(){
  Serial.print("&");
}

void loop(){  
  if(Serial.available() > 0){
    command = Serial.parseInt();
    switch(command){
      case 1:
        shutterOpen();
        captureImageGroup(); //send a string that represents 15 images to Serial for Python
        triggerEndRead();
      case 2:
        shutterStatus();
        triggerEndRead();
        break;
      case 3:
        shutterOpen(); // arbitrary argument. Replace after testing.!!!!!!!!!!!
        triggerEndRead();
        break;
      case 4:
        shutterClose();
        triggerEndRead();
        break;
      case 5:
        captureImage();
        triggerEndRead();
        break;
      case 6:
        showInternalTemp();
        triggerEndRead();
        break;
      default:
        Serial.println("INVALID command. Please try again.");
        triggerEndRead();
        break;
    }
  }
}
