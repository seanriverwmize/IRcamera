/* Photocell simple testing sketch. 
 
Connect one end of the photocell to 5V, the other end to Analog 0.
Then connect one end of a 10K resistor from Analog 0 to ground 
Connect LED from pin 11 through a resistor to ground 
For more information see http://learn.adafruit.com/photocells */
 
  void setup(void) {
    // Setup function needs to run once when instrument is plugged in
    Serial.begin(9600);   
  }
 
  bool shutterStatus(int minumum) { // "minimum" parameter is minumum analog reading when shutter is open
    int photocellPin = 0;            // more light on photocell means higher voltage reading on analog pin 0
    int photocellAnalogReading;     // the analog reading from the voltage divider
              
    photocellAnalogReading = analogRead(photocellPin); //analogRead converts Voltage value to an integer 0 - 1023 
    Serial.print("Analog reading = ");
    Serial.println(photocellAnalogReading);     // the raw analog reading prints to Serial
    if (photocellAnalogReading >= minimum){
    Serial.println("Shutter is Open");
    return true;
    } else {
    Serial.println("Shutter is Closed");
    return false;
    }
}
