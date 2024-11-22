#include <LiquidCrystal.h>
#include <Servo.h>

// Initialize the LCD
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Servo objects for azimuth and altitude
Servo servoAzimuth;
Servo servoAltitude;

// Celestial bodies
String celestialBodies[] = {
  "Mercury", "Venus", "Mars", "Jupiter", 
  "Saturn", "Uranus", "Neptune", 
  "Bennu", "Ceres", "2024 PT5"
};

int currentIndex = 0;
const int numBodies = sizeof(celestialBodies) / sizeof(celestialBodies[0]);

const int buttonUp = 8;
const int buttonDown = 9;
const int buttonSelect = 10;
const int buttonReset = 13; // Reset button

const unsigned long debounceDelay = 50;
unsigned long lastDebounceTimeUp = 0;
unsigned long lastDebounceTimeDown = 0;
unsigned long lastDebounceTimeSelect = 0;
unsigned long lastDebounceTimeReset = 0; // Reset button debounce

bool lastButtonStateUp = HIGH;
bool lastButtonStateDown = HIGH;
bool lastButtonStateSelect = HIGH;
bool lastButtonStateReset = HIGH; // Reset button state

String azimuthAltitude = "";
bool dataRequested = false;

const int REAL_TIME = 0;
const int PREDICTION = 1;

int modeIndex = REAL_TIME;
bool modeSelected = false;
bool celestialObjectSelected = false;
bool displayingAzAlt = false;

void setup() {
  lcd.begin(16, 2);
  pinMode(buttonUp, INPUT_PULLUP);
  pinMode(buttonDown, INPUT_PULLUP);
  pinMode(buttonSelect, INPUT_PULLUP);
  pinMode(buttonReset, INPUT_PULLUP);  // Set reset button as input with pull-up

  servoAzimuth.attach(6);
  servoAltitude.attach(7);

  Serial.begin(9600);

  displayModeSelection();
}

void loop() {
  unsigned long currentTime = millis();

  int readingUp = digitalRead(buttonUp);
  int readingDown = digitalRead(buttonDown);
  int readingSelect = digitalRead(buttonSelect);
  int readingReset = digitalRead(buttonReset); // Read reset button

  // Handle reset button press to reset and go back to mode selection
  if (readingReset != lastButtonStateReset) {
    lastDebounceTimeReset = currentTime;
    lastButtonStateReset = readingReset;
  }

  if ((currentTime - lastDebounceTimeReset) > debounceDelay && readingReset == LOW) {
    // Reset the whole system and go back to mode selection
    modeSelected = false;
    celestialObjectSelected = false;
    displayingAzAlt = false;
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("System Reset...");
    delay(1000); // Display reset message for 1 second
    displayModeSelection();
    return; // Exit early after handling the reset
  }

  // Up button handling
  if (readingUp != lastButtonStateUp) {
    lastDebounceTimeUp = currentTime;
    lastButtonStateUp = readingUp;
  }

  if ((currentTime - lastDebounceTimeUp) > debounceDelay && readingUp == LOW) {
    if (!modeSelected) {
      modeIndex = REAL_TIME;
      displayModeSelection();
    } else if (modeSelected && !celestialObjectSelected && !displayingAzAlt) {
      incrementIndex();
      displayCelestialBody();
    }
    delay(200);
  }

  // Down button handling
  if (readingDown != lastButtonStateDown) {
    lastDebounceTimeDown = currentTime;
    lastButtonStateDown = readingDown;
  }

  if ((currentTime - lastDebounceTimeDown) > debounceDelay && readingDown == LOW) {
    if (!modeSelected) {
      modeIndex = PREDICTION;
      displayModeSelection();
    } else if (modeSelected && !celestialObjectSelected && !displayingAzAlt) {
      decrementIndex();
      displayCelestialBody();
    }
    delay(200);
  }

  // Select button handling
  if (readingSelect != lastButtonStateSelect) {
    lastDebounceTimeSelect = currentTime;
    lastButtonStateSelect = readingSelect;
  }

  if ((currentTime - lastDebounceTimeSelect) > debounceDelay && readingSelect == LOW) {
    if (!modeSelected) {
      modeSelected = true;
      if (modeIndex == REAL_TIME) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Real-Time Mode");
        delay(1000);
        displayCelestialBody();
      } else if (modeIndex == PREDICTION) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Prediction Mode");
        delay(1000);
        Serial.println("Prediction");
        lcd.setCursor(0, 1);
        lcd.print("Triggering...");
        delay(2000);
        displayModeSelection();
      }
    } else if (modeSelected && !celestialObjectSelected) {
      celestialObjectSelected = true;
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Selected: ");
      lcd.print(celestialBodies[currentIndex]);

      Serial.println(celestialBodies[currentIndex]);

      long timeout = millis() + 20000;
      azimuthAltitude = "";

      while (millis() < timeout) {
        if (Serial.available() > 0) {
          azimuthAltitude = Serial.readStringUntil('\n');
          azimuthAltitude.trim();

          if (azimuthAltitude.indexOf(',') != -1) {
            displayingAzAlt = true;
            displayAzimuthAltitude();
            controlServos(azimuthAltitude);

            // Delay for 10 seconds after displaying azimuth and altitude
            delay(10000);
          } else {
            lcd.clear();
            lcd.setCursor(0, 0);
            lcd.print("Error/Timeout");
          }
          break;
        }
      }

      if (azimuthAltitude == "") {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Timeout/Error");
      }
      delay(2000);

      celestialObjectSelected = false;
      displayingAzAlt = false;
      displayCelestialBody();
    } else if (displayingAzAlt) {
      celestialObjectSelected = false;
      displayingAzAlt = false;
      displayCelestialBody();
    }
  }

  lastButtonStateUp = readingUp;
  lastButtonStateDown = readingDown;
  lastButtonStateSelect = readingSelect;
  lastButtonStateReset = readingReset; // Update reset button state
}

void incrementIndex() {
  currentIndex++;
  if (currentIndex >= numBodies) {
    currentIndex = 0;
  }
}

void decrementIndex() {
  currentIndex--;
  if (currentIndex < 0) {
    currentIndex = numBodies - 1;
  }
}

void displayCelestialBody() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(currentIndex + 1);
  lcd.print(": ");
  lcd.print(celestialBodies[currentIndex]);
}

void displayAzimuthAltitude() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Az/Alt:");
  lcd.setCursor(0, 1);
  lcd.print(azimuthAltitude);
}

void controlServos(String azAltData) {
  int commaIndex = azAltData.indexOf(',');
  if (commaIndex != -1) {
    String azimuthStr = azAltData.substring(0, commaIndex);
    String altitudeStr = azAltData.substring(commaIndex + 1);
    float azimuth = azimuthStr.toFloat();
    float altitude = altitudeStr.toFloat();

    moveServo(servoAzimuth, azimuth);
    moveServo(servoAltitude, altitude);
  }
}

void moveServo(Servo &servo, float angle) {
  angle = constrain(angle, 0, 180);
  servo.write(angle);
}

void displayModeSelection() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Select Mode:");
  lcd.setCursor(0, 1);
  if (modeIndex == REAL_TIME) {
    lcd.print("1: Real-Time");
  } else {
    lcd.print("2: Prediction");
  }
}
