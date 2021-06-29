String command;
void setup(void) {
  // Setup function needs to run once when instrument is plugged in
  Serial.begin(9600);   
}
void shutterStatus(int minumum) { // "minimum" parameter is minumum analog reading when shutter is open
  int photocellPin = 1;            // more light on photocell means higher voltage reading on analog pin 0
  int photocellAnalogReading;     // the analog reading from the voltage divider
            
  photocellAnalogReading = analogRead(photocellPin); //analogRead converts Voltage value to an integer 0 - 1023 
  Serial.print("Analog reading = ");
  Serial.println(photocellAnalogReading);     // the raw analog reading prints to Serial
  if (photocellAnalogReading >= minumum){
  Serial.println("Shutter is Open");
  //return true;
  } else {
  Serial.println("Shutter is Closed");
  //return false;
  }
}


void loop(){
//  shutterStatus(600);
//  delay(2000);  
  if(Serial.available() > 0){
    command = Serial.readString();
    Serial.print("Command: ");
    Serial.println(command);
    switch(command){
      case shutterStatusCase:
        shutterStatus(150);
        break;
      default:
        Serial.println("INVALID command. Please try again.");
        break;
    }
  }
}
