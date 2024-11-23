Here’s the README with all content included inside the code snippet while leaving the licensing details as instructed:  

```markdown
# **Real-Time Celestial Object Movement Tracking and Prediction System**

A system that tracks the real-time location and predicts the future movements of celestial objects with fair accuracy. It combines simplified calculation processes with a streamlined component setup.

> **📽️ Demo:** *Click [here](#) to view the project demo and computations.*

---

## **Table of Contents**
- [Installation](#installation)
- [Materials Required](#materials-required)
- [Steps for Construction](#steps-for-construction)
- [Usage](#usage)
  - [Setting up the System](#setting-up-the-system)
  - [Operating the LCD Interface](#operating-the-lcd-interface)
  - [Real-Time Mode](#using-real-time-mode)
  - [Prediction Mode](#using-prediction-mode)
- [Maintaining and Troubleshooting](#maintaining-and-troubleshooting)
- [Scope for Improvement](#scope-for-improvement)
- [Contributors](#contributors)

---

## **Materials Required**

| **Component**              | **Link**                                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------------------|
| 3 x Arduino Uno            | [Amazon](https://www.amazon.in/Arduino-Uno-Rev3-Microcontroller-Board/dp/B0752X52VB)                       |
| 16x2 LCD Display           | [Flipkart](https://www.flipkart.com/16x2-lcd-display-module-blue-backlight/p/itm0817793201)                |
| Push Button Switches       | [RobotShop](https://www.robotshop.com/en/products/taxibot-button-switch-normal-open?gclid=...)             |
| L298N Motor Driver IC      | [Amazon](https://www.amazon.in/L298N-Motor-Driver-Module-Dual-H-Bridge/dp/B07D3Y917R)                      |
| 28BYJ-48 5V DC Step Motors | [RobotShop](https://www.robotshop.com/en/products/pololu-37d-metal-gearmotor-100-1-37d-210rpm?gclid=...)  |
| Jumper Wires               | [Amazon](https://www.amazon.in/Jumper-Wire-Male-to-Female-20cm-20-Pcs/dp/B07D3Y917R)                       |
| Breadboard                 | [Amazon](https://www.amazon.in/ELECFY-Breadboard-830-Tie-Points-Self-Adhesive-PCB-Board/dp/B07D3Y917R)    |

---

## **Installation**

Install all the required Python dependencies with the following commands:  
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

---

## **Steps for Construction**

### **1. Construct the Circuit**

#### **1.1 Prepare the Arduino:**
- Mount the Arduino boards and connect them to your PC via USB.

#### **1.2 Connect the Azimuth Stepper Motor:**
Plug the azimuth stepper motor into the ULN2003 driver.  
| **Arduino Pin** | **ULN2003 Pin** |
|------------------|-----------------|
| D8               | IN1             |
| D9               | IN2             |
| D10              | IN3             |
| D11              | IN4             |
| 5V               | VCC             |
| GND              | GND             |

#### **1.3 Connect the Altitude Stepper Motor:**
Repeat the above steps for the altitude motor:  
| **Arduino Pin** | **ULN2003 Pin** |
|------------------|-----------------|
| D2               | IN1             |
| D3               | IN2             |
| D4               | IN3             |
| D5               | IN4             |
| 5V               | VCC             |
| GND              | GND             |

#### **1.4 Connect the LCD User Interface (Arduino 3):**

| **Arduino Pin** | **LCD Pin** |
|------------------|-------------|
| D12              | RS          |
| D11              | E           |
| D5               | D4          |
| D4               | D5          |
| D3               | D6          |
| D2               | D7          |
| 5V               | VCC         |
| GND              | GND         |

> **Note:**  
> Add a 10kΩ potentiometer for contrast control:
> - Connect one side to VCC, the other to GND, and the wiper pin to the LCD’s V0.

---

### **2. Test Connections**
Run the file `serial connection code.py` from your text editor or IDE to verify the setup.

---

## **Usage**

### **Setting up the System**
1. Ensure all hardware connections are secure.
2. Install the software dependencies listed in the [Installation](#installation) section.
3. Power the system via USB or an external supply.

### **Operating the LCD Interface**
1. **Start the System:**
   - Power on the LCD interface Arduino.
   - The LCD will display a welcome screen prompting you to select the mode.

2. **Select a Mode:**
   - Use the Up (D8) and Down (D9) buttons to scroll through options:
     - **Real-Time Mode**: Tracks celestial objects in real time.
     - **Prediction Mode**: Predicts future positions of celestial objects.
   - Press Select (D10) to confirm your choice.

---

### **Using Real-Time Mode**
1. **Navigate Celestial Objects:**
   - Use the buttons to scroll through a list of celestial bodies (e.g., Mercury, Venus, Mars).
   - Press Select (D10) to confirm your selection.

2. **Track the Object:**
   - The LCD displays the selected object's azimuth and altitude.
   - The motors align to point toward the object.

---

### **Using Prediction Mode**
1. **Trigger Prediction:**
   - Select "Prediction Mode" to begin.
   - Enter required observation values (dates, time, celestial object name).

2. **Analyze Results:**
   - View the system's predicted trajectory on the LCD and in a 3D browser plot.

---

## **Maintaining and Troubleshooting**

- **Motor Calibration**:  
   Swap motor connections if movement for positive/negative angles is reversed.

- **Serial Communication**:  
   Use the Arduino IDE's Serial Monitor to debug.

- **Hardware Checks**:  
   Ensure secure connections and adequate power supply for motors and servos.

---

## **Scope for Improvement**

1. Enhance prediction accuracy by integrating perturbation models.  
2. Adapt for tracking space debris.  
3. Add GPS for real-time location updates.  
4. Expand tracking to include deep-space objects.  
5. Design a weatherproof enclosure for outdoor use.

---

## **Contributors**

- **Vishnu Kumar K**: [vkneutromaster@gmail.com](mailto:vkneutromaster@gmail.com)  
- **Krish Praneeth G**: [gkrishpraneeth@gmail.com](mailto:gkrishpraneeth@gmail.com)  
``` 

Let me know if further refinements are needed! 🚀
