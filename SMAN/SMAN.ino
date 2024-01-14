// Define the pins for the 7-segment display
const int segmentPins[] = {12, 13, 14, 15, 16, 17, 18, 19};

// Set this to true if your 7-segment display is common cathode, false if common anode
const bool isCommonCathode = true;

int currentState = 0;

void setup() {
  // Initialize the segment pins as outputs
  for (int i = 0; i < 8; i++) {
    pinMode(segmentPins[i], OUTPUT);
  }
  Serial.begin(115200);
}

void displayNumber(int number) {
  // Define the 7-segment patterns for each digit
  const int digitPatterns[11][8] = {
    {LOW, LOW, LOW, LOW, LOW, LOW, HIGH, HIGH},  // 0
    {HIGH, LOW, LOW, HIGH, HIGH, HIGH, HIGH, HIGH},  // 1
    {LOW, LOW, HIGH, LOW, LOW, HIGH, LOW, HIGH},  // 2
    {LOW, LOW, LOW, LOW, HIGH, HIGH, LOW, HIGH},  // 3
    {HIGH, LOW, LOW, HIGH, HIGH, LOW, LOW, LOW},  // 4
    {LOW, HIGH, LOW, LOW, HIGH, LOW, LOW, LOW},  // 5
    {LOW, HIGH, LOW, LOW, LOW, LOW, LOW, LOW},  // 6
    {LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH, HIGH},  // 7
    {LOW, LOW, LOW, LOW, LOW, LOW, LOW, HIGH},  // 8
    {LOW, LOW, LOW, LOW, HIGH, LOW, LOW, HIGH},   // 9
    {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH,}   // DULL
  };

  // Display each digit based on the current state
  for (int i = 0; i < 8; i++) {
    if (isCommonCathode) {
      digitalWrite(segmentPins[i], digitPatterns[number][i]);
    } else {
      digitalWrite(segmentPins[i], !digitPatterns[number][i]);
    }
  }
  delay(1000); // Adjust the delay as needed
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming message
    String message = Serial.readStringUntil('\n');

    // Check the content of the message and update the current state
    if (message == "A") {
      currentState = 1;
    } else if (message == "B") {
      currentState = 2;
    } else if (message == "C") {
      currentState = 3;
    } else if (message == "D") {
      currentState = 4;
    } else if (message == "E") {
      currentState = 5;
    } else if (message == "F") {
      currentState = 6;
    } else if (message == "G") {
      currentState = 7;
    } else if (message == "H") {
      currentState = 8;
    } else if (message == "I") {
      currentState = 9;
    }
  }

  // Display the current state directly
  if (currentState >= 0 && currentState <= 9) {
    displayNumber(currentState);
  }
}
