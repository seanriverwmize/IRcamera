#include <Stepper.h>

// change this to the number of steps on your motor
#define STEPS 200

// create an instance of the stepper class, specifying
// the number of steps of the motor and the pins it's
// attached to
Stepper stepper(STEPS, 12, 11, 9, 7); //Pins used in order: AIN1, AIN2, BIN2, BIN1


void setup() // Setup runs once when the instrument is powered on
{
  Serial.begin(9600);
  stepper.setSpeed(60); // set the speed of the motor to 30 RPMs
}

void shutterOpen(int motorSteps)// parameter = number of 1/200 rotations motor will make if shutter is closed. param should be replaced with concrete value after testing
{
  if (shutterStatus() == false)   // If shutter is closed, rotate motor. Otherwise, end function.
    stepper.step(motorSteps);   // Squiggly brackets not need with only one statement.
}
