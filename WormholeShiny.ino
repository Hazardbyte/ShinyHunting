#include <Servo.h>

// create servo objects
Servo servoAButton;
Servo servoStartButton;

bool keepLooping = true;
int foo = 1;

void setup() {
  foo++;
  servoAButton.attach(3); // attaches the servo on pin 5 to the servo object
  servoStartButton.attach(8);  // attaches the servo on pin 3 to the servo object
  
  Serial.begin(9600); // open a serial connection to your computer
  Serial.print ("We Ready...\n");
}

// Holds the A button down for the specified amount of milliseconds. pressDurationInMS should be at least 100 for best results.
void pressAButton(int pressDurationInMS) {
  servoAButton.write(155); // set servo angle. First contact with A Button
  delay(pressDurationInMS);   // wait
  servoAButton.write(100); // set servo angle. Pulling away from A Button
}

// Holds the Start button down for the specified amount of milliseconds. pressDurationInMS should be at least 100 for best results.
void pressStartButton(int pressDurationInMS) {
  servoStartButton.write(120); // set servo angle. First Contact with Start Button
  delay(pressDurationInMS);       // wait
  servoStartButton.write(0); // set servo angle. Pulling away from Start Button
}


void loop() {
  delay(5000); // wait 5 seconds before start of program
  servoAButton.write(0); // set servo angle. First contact with A Button
  servoStartButton.write(0);

  if(keepLooping){
      Serial.println("Starting Loop");
      
      Serial.println("First A click");
      pressAButton(500);
      Serial.println("Waiting for Select Screen");
      delay(2800);
      Serial.println("Clicking on the save file");
      pressAButton(500);
      delay(11000);
      
      Serial.println("Flushing leftover data");
      while (Serial.available() != 0) {
        char t = Serial.read();
      }

      // Send message to Python
    Serial.println("Command: checkIfShiny");
    Serial.println("taking shiny pic");
    
    // Wait until we receive a message from Python
    while (Serial.available() == 0) {
      delay(200);
    }
    
    Serial.println("Reading response from Python");
    Serial.println("Reading response from Python");

    
    // Read response from Python
    char inByte = Serial.read();
    
    // Check if shiny
    if (inByte == 'y') {
      // it's shiny! Stop looping
      
      Serial.println("It's shiny!");
      keepLooping = false;
    }else{
      // not shiny. Do a soft reset and keep on looping!

      Serial.println("Not shiny. Doing soft reset");
      keepLooping = true;
      pressStartButton(200);
      
      // wait 5 seconds after soft reset
      delay(5000);
    }
  }
}
