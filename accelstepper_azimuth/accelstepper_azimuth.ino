#include <Stepper.h>

const int stepsPerRevolution = 2048;
const float degreesPerStep = 360.0 / stepsPerRevolution;
Stepper azimuthStepper(stepsPerRevolution, 8, 9, 10, 11);
int azimuthCurrentStepPosition = 0;

void setup() {
    Serial.begin(9600);
    azimuthStepper.setSpeed(7); // Set speed of 7 RPM
}

void loop() {
    if (Serial.available() > 0) {
        // Read mode ('R' or 'P') with small delay for all data to arrive
        char mode = Serial.read();
        delay(10); 

        if (mode == 'R') {
            int targetAngle = Serial.parseInt(); // Real-Time single angle movement
            int targetSteps = targetAngle / degreesPerStep;
            azimuthStepper.step(targetSteps - azimuthCurrentStepPosition);
            azimuthCurrentStepPosition = targetSteps;
            delay(10000); // Settle

            // Return to origin
            azimuthStepper.step(-azimuthCurrentStepPosition);
            azimuthCurrentStepPosition = 0;

        } else if (mode == 'P') {
            // Prediction mode, requires initial and final angles
            int initialAngle = Serial.parseInt();
            delay(10); // Delay between readings
            int finalAngle = Serial.parseInt();

            int initialSteps = initialAngle / degreesPerStep;
            int finalSteps = finalAngle / degreesPerStep;

            // Move to initial angle
            azimuthStepper.step(initialSteps - azimuthCurrentStepPosition);
            azimuthCurrentStepPosition = initialSteps;
            delay(5000); // Wait

            // Move to final angle
            int stepDifference = finalSteps - initialSteps;
            azimuthStepper.step(stepDifference);
            azimuthCurrentStepPosition += stepDifference;
            delay(5000); // Wait

            // Return to origin
            azimuthStepper.step(-azimuthCurrentStepPosition);
            azimuthCurrentStepPosition = 0;
        }
    }
}
