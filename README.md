# Real-Time Celestial Object Movement Tracking and Prediction System
A system that tracks and predicts the real-time location of celestial objects with simplified calculations and component setup. To view the project demo and the computations, please click [here](https://tinyurl.com/celestialtracker).

---

## Table of Contents
- [Installation](#installation)
- [Materials Required](#materials-required)
- [Steps for Construction](#steps-for-construction)
- [Usage](#usage)
- [Scope for Improvement](#scope-for-improvement)
- [Contributors](#contributors)
- [License](#license)

---

## Materials Required 
| Component                      | Link |
|---------------------------------|------|
| 3 X Arduino Uno                 | [Amazon](https://www.amazon.in/Arduino-Uno-Rev3-Microcontroller-Board/dp/B0752X52VB) |
| 16x2 LCD Display                | [Flipkart](https://www.flipkart.com/16x2-lcd-display-module-blue-backlight/p/itm0817793201) |
| Push Button Switches            | [RobotShop](https://www.robotshop.com/en/products/taxibot-button-switch-normal-open?utm_source=google_shopping&utm_medium=cpc&utm_campaign=shopping_en&gclid=CjwKCAjw864v7E9z8-YcAXoQBAv410nX0Y2o433p9Y3gX9X8_3bY3z7l_909q9p7F5aApS_wcB) |
| L298N Motor Driver IC           | [Amazon](https://www.amazon.in/L298N-Motor-Driver-Module-Dual-H-Bridge/dp/B07D3Y917R) |
| 28BYJ-48 5V DC Step Motors      | [RobotShop](https://www.robotshop.com/en/products/pololu-37d-metal-gearmotor-100-1-37d-210rpm?utm_source=google_shopping&utm_medium=cpc&utm_campaign=shopping_en&gclid=CjwKCAjw864v7E9z8-YcAXoQBAv410nX0Y2o433p9Y3gX9X8_3bY3z7l_909q9p7F5aApS_wcB) |
| Jumper Wires                    | [Amazon](https://www.amazon.in/Jumper-Wire-Male-to-Female-20cm-20-Pcs/dp/B07D3Y917R) |
| Breadboard                      | [Amazon](https://www.amazon.in/ELECFY-Breadboard-830-Tie-Points-Self-Adhesive-PCB-Board-Arduino-Raspberry-Pi-Projects/dp/B07D3Y917R) |

---

## Installation:
Install the required dependencies:
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

### 1. Construct the Circuit
#### Prepare the Arduino:
- Mount the Arduino boards and connect them to your PC via USB.

#### Connect the Azimuth Stepper Motor:
Plug the azimuth stepper motor into the ULN2003 driver.
| Arduino Pin | ULN2003 Pin |
|-------------|-------------|
| D8          | IN1         |
| D9          | IN2         |
| D10         | IN3         |
| D11         | IN4         |
| 5V          | VCC         |
| GND         | GND         |

#### Connect the Altitude Stepper Motor:
Repeat the steps for the altitude stepper motor:
| Arduino Pin | ULN2003 Pin |
|-------------|-------------|
| D2          | IN1         |
| D3          | IN2         |
| D4          | IN3         |
| D5          | IN4         |
| 5V          | VCC         |
| GND         | GND         |

**Note**: To enable counterclockwise rotation, swap the connections as needed.

#### Connect the LCD User Interface (Arduino 3):
- Connect the LCD to the third Arduino and attach buttons for mode and celestial object selection.
  
| Arduino Pin | LCD Pin  |
|-------------|----------|
| D12         | RS       |
| D11         | E        |
| D5          | D4       |
| D4          | D5       |
| D3          | D6       |
| D2          | D7       |
| 5V          | VCC      |
| GND         | GND      |

**Buttons**:
| Arduino Pin | Button    |
|-------------|-----------|
| D8          | ButtonUp  |
| D9          | ButtonDown|
| D10         | ButtonSelect|
| D13         | ButtonReset|

#### Power the Arduinos:
- If running on USB power, ensure all Arduinos are connected to separate USB ports.
- For external power supply, connect 5V DC to ULN2003 VCC pins.

---

### 2. Create an Elegant Case
- **LCD Interface**: Cut holes in a box for buttons and the LCD display. Enclose the circuit and fix the components in place.
- **Celestial Object Locator**: Mount motors on a tripod and attach a stick for azimuth and altitude alignment.

---

## Usage

### Setting up the System
1. Verify hardware connections.
2. Install software dependencies and upload codes.
3. Power on the system.

---

### Operating the LCD Interface
1. **Start the System**: The LCD will display a welcome screen and prompt for mode selection.
2. **Select the Mode**: Use Up/Down buttons to choose between:
   - **Real-Time Mode**: Track celestial objects in real-time.
   - **Prediction Mode**: Predict celestial object positions.

---

### Using Real-Time Mode
1. **Navigate Celestial Objects**: Scroll through the list and select an object.
2. **Track Object**: The LCD shows "Tracking <object name>" and adjusts motor positions.
3. **View Results**: Observe the motors aligning with the object.
4. **Reset/ Switch**: Press Reset to return to the mode selection.

---

### Using Prediction Mode
1. **Trigger Prediction**: The LCD shows "Triggering Prediction." Enter values such as object name and observation dates.
2. **Enter Values**: Provide observation start/stop dates and prediction times.
3. **Observe and Record**: The system predicts positions and updates the motors and 3D visualization.

### Maintaining and Troubleshooting
1. **Calibrate Motors**: Test and ensure both motors move in the correct direction for positive and negative angles. If the movement is incorrect, swap the motor connections and re-test.

2. **Debug Serial Communication**: Use the Arduino IDE's Serial Monitor to verify that each Arduino correctly receives data from the Python program.

3. **Reset for Errors**: If any issue arises during tracking or prediction, press the Reset (D13) button to return to the main menu.
   
4. **Check Hardware Connections**: Ensure all wires and connections are secure. Verify that the power supply is adequate for the motors and servos.

5. **Note**: To enable the functionality of rotating the shaft anticlockwise for the altitude and azimuth stepper motors when pointing at celestial bodies or tracing their orbits, interchange the connections of the motor's input ports to the Arduino's Digital ports. Test-run the code to check if the motors move anticlockwise. Iterate until the desired movement is achieved. One of the motors must move anticlockwise for positive angles, and for negative angles, similarly.

---

## Scope for Improvement
1. **Accuracy Enhancements**: Incorporate more accurate orbital mechanics and real-time GPS for location updates.
2. **Space Debris Tracking**: Modify the system to monitor space debris.
3. **Advanced Sensors**: Add gyroscopic/accelerometer sensors for precise positioning.
4. **Deep-Space Objects**: Extend the system to track exoplanets, comets, etc.
5. **Portability**: Design a weatherproof enclosure for outdoor use.
6. **Multi-Object Tracking**: Support multiple object tracking with additional motors.
7. **User Accessibility**: Integrate voice control or a smartphone app.
8. **Renewable Power**: Power the system using solar energy for sustainability.

---

## Contributors
- **Krish Praneeth G**  
- **Vishnu Kumar K**

**Contact the creators**:  
Vishnu Kumar K  
> vkneutromaster@gmail.com  
Krish Praneeth G  
> gkrishpraneeth@gmail.com
