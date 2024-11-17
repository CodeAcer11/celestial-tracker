#include <Stepper.h>

const int stepsPerRevolution = 2048;
const float degreesPerStep = 360.0 / stepsPerRevolution;
Stepper altitudeStepper(stepsPerRevolution, 8, 9, 10, 11);
int altitudeCurrentStepPosition = 0;

void setup() {
    Serial.begin(9600);
    altitudeStepper.setSpeed(7); // Set speed of 7 RPM
}

void loop() {
    if (Serial.available() > 0) {
        // Read mode ('R' or 'P') with small delay for all data to arrive
        char mode = Serial.read();
        delay(10);

        if (mode == 'R') {
            int targetAngle = Serial.parseInt(); // Real-Time single angle movement
            int targetSteps = targetAngle / degreesPerStep;
            altitudeStepper.step(targetSteps - altitudeCurrentStepPosition);
            altitudeCurrentStepPosition = targetSteps;
            delay(10000); // Settle

            // Return to origin
            altitudeStepper.step(-altitudeCurrentStepPosition);
            altitudeCurrentStepPosition = 0;

        } else if (mode == 'P') {
            // Prediction mode, requires initial and final angles
            int initialAngle = Serial.parseInt();
            delay(10); // Delay between readings
            int finalAngle = Serial.parseInt();

            int initialSteps = initialAngle / degreesPerStep;
            int finalSteps = finalAngle / degreesPerStep;

            // Move to initial angle
            altitudeStepper.step(initialSteps - altitudeCurrentStepPosition);
            altitudeCurrentStepPosition = initialSteps;
            delay(5000); // Wait

            // Move to final angle
            int stepDifference = finalSteps - initialSteps;
            altitudeStepper.step(stepDifference);
            altitudeCurrentStepPosition += stepDifference;
            delay(5000); // Wait

            // Return to origin
            altitudeStepper.step(-altitudeCurrentStepPosition);
            altitudeCurrentStepPosition = 0;
        }
    }
}

