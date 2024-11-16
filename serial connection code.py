import serial
import time
import subprocess  # For running external Python files
from astroquery.jplhorizons import Horizons
from astropy.time import Time
from astropy.coordinates import EarthLocation
import numpy as np
import astropy.units as u

# Define location coordinates
latitude = 13.1453
longitude = 80.4514
elevation = 6

# Dictionary mapping celestial bodies to their Horizons ID
celestial_objects = {
    'Sun': '10',
    'Moon': '301',
    'Mercury': '199',
    'Venus': '299',
    'Mars': '499',
    'Jupiter': '599',
    'Saturn': '699',
    'Uranus': '799',
    'Neptune': '899',
    'Bennu': '101955',
    'Ceres': '1',
    '2024 PT5': 'DES=2024 PT5'
}

def get_azimuth_altitude(celestial_id):
    """Get azimuth and altitude for a celestial object."""
    time_now = Time.now()
    location = EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m)

    try:
        epochs = [time_now.jd]
        object_ephem = Horizons(id=celestial_id, location=f'{longitude},{latitude}', epochs=epochs).ephemerides()[0]
        ra_object = object_ephem['RA']
        dec_object = object_ephem['DEC']
        print(f"Horizons Response: RA={ra_object}, DEC={dec_object}")
    except Exception as e:
        print(f"Error querying Horizons for {celestial_id}: {e}")
        return None, None

    # Calculate hour angle H
    lst = time_now.sidereal_time('apparent', longitude=location.lon)
    H = (lst - ra_object * u.deg).to(u.deg)

    # Convert to radians for trigonometric functions
    phi = np.radians(latitude)
    delta = np.radians(dec_object)
    H_rad = np.radians(H.value)

    # Calculate altitude
    sin_alt = np.sin(delta) * np.sin(phi) + np.cos(delta) * np.cos(phi) * np.cos(H_rad)
    altitude = np.degrees(np.arcsin(sin_alt))

    # Calculate azimuth
    sin_A = -np.sin(H_rad) * np.cos(delta)
    cos_A = (np.sin(delta) - np.sin(phi) * np.sin(np.radians(altitude))) / (np.cos(phi) * np.cos(np.radians(altitude)))
    azimuth = np.degrees(np.arctan2(sin_A, cos_A))
    if azimuth < 0:
        azimuth += 360

    return azimuth, altitude

def run_prediction_system():
    """Run the prediction system and wait for it to close."""
    try:
        subprocess.run(["python", "C:\\Users\\gkris\Downloads\\all files_celestial tracking system\\all files_celestial tracking system\\prediction system.py"], check=True)
        print("Prediction system executed and closed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the Python prediction system: {e}")

def reopen_serial_connections():
    """Reopen serial connections after prediction system execution."""
    try:
        ser_lcd = serial.Serial('COM4', 9600, timeout=5)  # LCD/UI communication (COM9)
        ser_azimuth = serial.Serial('COM6', 9600, timeout=5)  # Azimuth motor control (COM7)
        ser_altitude = serial.Serial('COM3', 9600, timeout=5)  # Altitude motor control (COM8)
        time.sleep(2)  # Allow time for connections to establish
        print("Serial connections reopened.")
        return ser_lcd, ser_azimuth, ser_altitude
    except serial.SerialException as e:
        print(f"Error: Cannot reopen serial ports. {e}")
        return None, None, None

def main():
    """Main function to handle communication over serial connections."""
    try:
        # Open the initial serial connections
        ser_lcd = serial.Serial('COM4', 9600, timeout=5)  # LCD/UI communication (COM9)
        ser_azimuth = serial.Serial('COM3', 9600, timeout=5)  # Azimuth motor control (COM7)
        ser_altitude = serial.Serial('COM6', 9600, timeout=5)  # Altitude motor control (COM8)
        time.sleep(2)  # Allow time for connections to establish
    except serial.SerialException as e:
        print(f"Error: Cannot open serial ports. {e}")
        return

    try:
        while True:
            if ser_lcd.in_waiting > 0:
                selected_object = ser_lcd.readline().decode('utf-8').strip()
                print(f"Selected object: {selected_object}")

                if selected_object in celestial_objects:
                    celestial_id = celestial_objects[selected_object]
                    azimuth, altitude = get_azimuth_altitude(celestial_id)

                    if azimuth is not None and altitude is not None:
                        # Send mode and azimuth to Azimuth motor
                        ser_azimuth.write(b'R\n')  # Send Real-Time mode character first
                        ser_azimuth.write(f"{azimuth:.2f}\n".encode())  # Send azimuth value
                        ser_azimuth.flush()
                        print(f"Sent to Azimuth Motor: Mode: R, Azimuth: {azimuth:.2f}")

                        # Send mode and altitude to Altitude motor
                        ser_altitude.write(b'R\n')  # Send Real-Time mode character first
                        ser_altitude.write(f"{altitude:.2f}\n".encode())  # Send altitude value
                        ser_altitude.flush()
                        print(f"Sent to Altitude Motor: Mode: R, Altitude: {altitude:.2f}")

                        # Send data to LCD
                        ser_lcd.write(f" {azimuth:.2f}, {altitude:.2f}\n".encode())
                        ser_lcd.flush()
                        print(f"Sent to LCD: Az: {azimuth:.2f}, Alt: {altitude:.2f}")

                    else:
                        ser_lcd.write(b"Error: Invalid data\n")
                        ser_lcd.flush()
                        print("Sent to LCD: Error: Invalid data")

                elif selected_object == "Prediction":
                    # Close serial connections before running prediction system
                    ser_lcd.close()
                    ser_azimuth.close()
                    ser_altitude.close()
                    print("Serial connections closed before prediction execution.")

                    # Run the prediction system and wait for it to close
                    run_prediction_system()

                    # Reopen serial connections after prediction system execution
                    ser_lcd, ser_azimuth, ser_altitude = reopen_serial_connections()
                    if not ser_lcd or not ser_azimuth or not ser_altitude:
                        print("Unable to reopen serial connections, exiting.")
                        break
                else:
                    ser_lcd.write(b"Invalid object\n")
                    ser_lcd.flush()
                    print("Sent to LCD: Invalid object")
            time.sleep(0.5)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure serial ports are closed in case of an unhandled exception
        if ser_lcd and ser_lcd.is_open:
            ser_lcd.close()
        if ser_azimuth and ser_azimuth.is_open:
            ser_azimuth.close()
        if ser_altitude and ser_altitude.is_open:
            ser_altitude.close()
        print("Serial connections closed.")

if __name__ == '__main__':
    main()
