#include <Arduino.h>

const int xAxisPin = A0; // Joystick X-axis connected to A0
const int buttonPin = 2; // Button connected to digital pin 2
const int potPin = A2;   // Potentiometer connected to A2
bool buttonPressed = false; // Track if the button was pressed

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP); // Assuming active-low button
}

void loop() {
  int xAxisValue = analogRead(xAxisPin);
  int buttonState = digitalRead(buttonPin);
  int potValue = analogRead(potPin); // Read the potentiometer value

  // Map the joystick X-axis to a MIDI note range (e.g., 48 to 72 for C2 to C4)
  int note = map(xAxisValue, 0, 1023, 48, 72);
  
  // Map the potentiometer value to the MIDI modulation range (0 to 127)
  int modulation = map(potValue, 0, 1023, 0, 127);

  // Send joystick X-axis position, button state, and modulation value over serial
  Serial.print("N"); Serial.print(note);
  Serial.print("B"); Serial.print(buttonState);
  Serial.print("M"); Serial.println(modulation); // Send modulation value

  delay(100); // Adjust delay as needed
}
