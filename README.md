# Real-Time Celestial Object Movement Tracking and Prediction System
A system that aims to track the real-time location and predict the future movements of celestial objects with a fair amount of accuracy using a simplified calculation process and component setup. To view the project demo, and the computations please click here.

## Table of Contents
- [Installation](#installation)
- [Materials Required](#materials-required)
- [Steps for Construction](#steps-for-construction)
- [Usage](#usage)
- [Scope for Improvement](#scope-for-improvement)
- [Contributors](#contributors)
- [License](#license)

## Materials Required 
| Component | Link |
|---|---|
| 3 X Arduino Uno | [Amazon](https://www.amazon.in/Arduino-Uno-Rev3-Microcontroller-Board/dp/B0752X52VB) |
| 16x2 LCD Display | [Flipkart](https://www.flipkart.com/16x2-lcd-display-module-blue-backlight/p/itm0817793201) |
| Push Button Switches | [RobotShop](https://www.robotshop.com/en/products/taxibot-button-switch-normal-open?utm_source=google_shopping&utm_medium=cpc&utm_campaign=shopping_en&gclid=CjwKCAjw864v7E9z8-YcAXoQBAv410nX0Y2o433p9Y3gX9X8_3bY3z7l_909q9p7F5aApS_wcB) |
| L298N Motor Driver IC | [Amazon](https://www.amazon.in/L298N-Motor-Driver-Module-Dual-H-Bridge/dp/B07D3Y917R) |
| 28BYJ-48 5V DC Step Motors | [RobotShop](https://www.robotshop.com/en/products/pololu-37d-metal-gearmotor-100-1-37d-210rpm?utm_source=google_shopping&utm_medium=cpc&utm_campaign=shopping_en&gclid=CjwKCAjw864v7E9z8-YcAXoQBAv410nX0Y2o433p9Y3gX9X8_3bY3z7l_909q9p7F5aApS_wcB) |
| Jumper Wires | [Amazon](https://www.amazon.in/Jumper-Wire-Male-to-Female-20cm-20-Pcs/dp/B07D3Y917R) |
| Breadboard | [Amazon](https://www.amazon.in/ELECFY-Breadboard-830-Tie-Points-Self-Adhesive-PCB-Board-Arduino-Raspberry-Pi-Projects/dp/B07D3Y917R) |

## Installation:
Install dependencies:
```bash
pip install numpy
pip install astropy
pip install skycoord
pip install plotly
pip install tkinter
pip install sqlite3
pip install scipy
pip install astroquery
pip install threading
```

## Steps for Construction
### Construct the Circuit
1. Prepare the Arduino:
Mount the Arduino boards and connect them to your PC via USB.

2. Connect the Azimuth Stepper Motor:
Plug the azimuth stepper motor into the ULN2003 driver.

| Arduino Pin | ULN2003 Pin |
|---|---|
| D8 | IN1 |
| D9 | IN2 |
| D10 | IN3 |
| D11 | IN4 |
| 5V | VCC |
| GND | GND |

3. Connect the Altitude Stepper Motor:
Repeat the above steps for the altitude stepper motor:

| Arduino Pin | ULN2003 Pin |
|---|---|
| D2 | IN1 |
| D3 | IN2 |
| D4 | IN3 |
| D5 | IN4 |
| 5V | VCC |
| GND | GND |

**`Note`** To enable the functionality of rotating the shaft anticlockwise, for the altitude and azimuth stepper motors, when pointing at the location of celestial bodies, or when tracing their orbit (in the case of the prediction system), interchange the connections of the input ports of the motor to Digital ports of the Arduino, and test run the code to check if the motors move anticlockwise, iterate till the desired movement is achieved. (When testing for positive angles, one of the motors must move anticlockwise, and the other must, for negative angles similarly.)

4. Connect the LCD User Interface (Arduino 3):
Hardware Setup:
> Connect the 16x2 LCD directly to the third Arduino.
> Attach push buttons for mode and celestial object selection.
> Connect servo motors for azimuth and altitude to control based on received data.

> Connections for LCD:
RS → D12
E → D11
D4 → D5
D5 → D4
D6 → D3
D7 → D2
LCD VCC → Arduino 5V pin.
LCD GND → Arduino GND pin.

> Connect a 10kΩ potentiometer for contrast:
One side to VCC, one side to GND, and the middle wiper pin to LCD V0.

> Connections for Buttons:
ButtonUp → D8
ButtonDown → D9
ButtonSelect → D10
ButtonReset → D13
The other side of each button to GND.
Use Arduino’s internal pull-up resistors.

> Connections for Servos:
ServoAzimuth (signal pin) → D6.
ServoAltitude (signal pin) → D7.
Servo VCC → Arduino 5V pin.
Servo GND → Arduino GND pin.


5. Power the Arduinos:
> If running on USB power:
Ensure the three Arduinos are connected to your PC, via three different USB ports. This is only possible in computers with at least 3 ports. Make sure the motors are connected to USB 3.0 ports, and the LCD Interface Circuit to the other port, if available, to ensure efficient power supply.
> If using an external power supply:
Connect 5V DC to the ULN2003 VCC pins and ensure the GND is common with the Arduino.

6. Test Connections:
Once all 3 Arduino circuits are connected to the computer, test the code by running the file 'serial connection code.py' in a text editor or IDE.

### Create an Elegant Case
1. LCD User Interface
- Pierce 4 circular holes on the larger face of a cuboidal cardboard box, to make the process simple
- Cut out a rectangular hole on the same face, to fit the LCD just enough
- Enclose the Arduino circuit in which the LCD is connected, in the box, and fix the buttons and the display in their appropriate positions.
- Decorate the model for a sleek appearance.

2. Celestial Object Locator
- Mount the azimuth motor on a tripod stand, and carefully glue a circular piece of cardboard to the motor's shaft. [The model can work without a tripod too]
- Glue the altitude motor's base on this cardboard such that the shaft of the motor is horizontally in line with ground level (geographical horizon).
- Attach a toothpick or a wooden stick of desired length to the shaft of the altitude motor such that it points towards the direction from which when tested, the motor moves upward for positive altitude angle values, and downward for negative altitude angle values.
- Stick a compass if needed, to the tripod, to aid in orienting the altitude motor's pointing needle towards north.

Real-Time Celestial Object Movement Tracking and Prediction System is now ready to use.

## Usage

## Scope for Improvement
1. Enhance Accuracy of Predictions:
> Incorporate more accurate orbital mechanics using perturbation models for a better representation of celestial orbits.
> Integrate a GPS module for real-time observer location updates to improve azimuth and altitude calculations.

> Adapt for Space Debris Tracking:
Modify the system to monitor and predict the location of space debris, providing valuable assistance to satellite operators and researchers.

> Integrate Advanced Sensors:
Add gyroscopic and accelerometer sensors to the motors for more precise angular positioning.

> Expand Usability to Deep-Space Objects:
Include calculations for far-away celestial objects like exoplanets, quasars, or comets.

> Portability and Weatherproofing:
Design a compact, weather-resistant enclosure for outdoor use under varying weather conditions.

> Multi-Object Tracking:
Allow simultaneous tracking of multiple celestial bodies by integrating additional stepper motors and a modular motor driver system.

> User Accessibility:
Add voice recognition or smartphone app control for seamless user interaction.

> Renewable Power Integration:
Power the system using solar panels or other renewable energy sources for sustainability.

## Contributors
Krish Praneeth G, Vishnu Kumar K
**`Contact the creators:`**
Vishnu Kumar K
> vkneutromaster@gmail.com

Krish Praneeth G
> 


## Licence
