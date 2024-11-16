import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import sqlite3
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
import astropy.units as u
from astroquery.exceptions import InvalidQueryError
import numpy as np
from astroquery.jplhorizons import Horizons
from scipy.integrate import odeint
import plotly.graph_objs as go  
import plotly.io as pio
import os
import webbrowser
import serial
import queue
import time as pytime

# Database setup and connection
try:
    conn = sqlite3.connect('asteroid_orbit.db', check_same_thread=False)
    cur = conn.cursor()
except sqlite3.Error as e:
    print(f"Database connection failed: {e}")
    exit(1)

# Constants
G = 6.674e-11  # Gravitational constant (m^3 kg^-1 s^-2)
M_sun = 1.989e30  # Mass of the Sun (kg)
AU = 1.496e11  # Astronomical unit (m)
latitude = 13.041007  # Observer latitude in degrees
longitude = 80.199432  # Observer longitude in degrees
elevation = 6  # Elevation in meters

# Serial setup for communication with Arduino
try:
    ser_azimuth = serial.Serial('COM3', 9600, timeout=5)
    ser_altitude = serial.Serial('COM6', 9600, timeout=5)
except Exception as e:
    print(f"Error connecting to serial port: {e}")
    ser = None

# Tkinter UI setup

root = tk.Tk()
root.title("Celestial Body Movement Prediction System")

# Add a title and subtitle
title_label = tk.Label(root, text="Celestial Body Movement Prediction System", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

subtitle_label = tk.Label(root, text="A project by Vishnu Kumar K & Krish Praneeth G", font=("Arial", 10, "italic"))
subtitle_label.grid(row=1, column=0, columnspan=2)

# Create frames for input and output
input_frame = tk.Frame(root)
input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="n")

output_frame = tk.Frame(root)
output_frame.grid(row=2, column=1, padx=10, pady=10, sticky="n")

# Entry fields
tk.Label(input_frame, text="Celestial Body Name:").pack()
asteroid_entry = tk.Entry(input_frame)
asteroid_entry.pack()

tk.Label(input_frame, text="Observation Start Date (YYYY-MM-DD):").pack()
start_entry = tk.Entry(input_frame)
start_entry.pack()

tk.Label(input_frame, text="Observation Stop Date (YYYY-MM-DD):").pack()
stop_entry = tk.Entry(input_frame)
stop_entry.pack()

tk.Label(input_frame, text="Observation Stop Time (HH:MM):").pack()
stop_time_entry = tk.Entry(input_frame)
stop_time_entry.pack()

tk.Label(input_frame, text="Prediction End Date (YYYY-MM-DD):").pack()
end_entry = tk.Entry(input_frame)
end_entry.pack()

tk.Label(input_frame, text="Prediction End Time (HH:MM):").pack()
end_time_entry = tk.Entry(input_frame)
end_time_entry.pack()

# temp code
#asteroid_entry=tk.Entry(input_frame)
# start_entry=tk.Entry(input_frame)
# stop_entry=tk.Entry(input_frame)
# stop_time_entry=tk.Entry(input_frame)
# end_entry=tk.Entry(input_frame)
# end_time_entry=tk.Entry(input_frame)

# Output display
output_display = ScrolledText(output_frame, wrap=tk.WORD, height=10, width=50)
output_display.pack()
output_display.config(state=tk.DISABLED)

# Create a queue for thread-safe communication
message_queue = queue.Queue()

# Treeview for data table with scrollbar
tree_frame = tk.Frame(output_frame)
tree_frame.pack()

tree_scroll = tk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

data_table = ttk.Treeview(tree_frame, columns=('Time', 'Position', 'Velocity', 'Azimuth', 'Altitude'), show='headings', height=10, yscrollcommand=tree_scroll.set)
tree_scroll.config(command=data_table.yview)

data_table.heading('Time', text='Timestamp')
data_table.heading('Position', text='Position (AU)')
data_table.heading('Velocity', text='Velocity (m/s)')
data_table.heading('Azimuth', text='Azimuth (deg)')
data_table.heading('Altitude', text='Altitude (deg)')
data_table.pack()

# Progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=400)
progress_bar.grid(row=4, column=0, columnspan=2, pady=10)

# Function to append text to ScrolledText in a thread-safe way
def append_text(text):
    output_display.config(state=tk.NORMAL)
    output_display.insert(tk.END, text + "\n")
    output_display.see(tk.END)
    output_display.config(state=tk.DISABLED)

# Function to clear the table before each prediction
def clear_table():
    for row in data_table.get_children():
        data_table.delete(row)

# Send azimuth and altitude to Arduino
import serial
import time

# Persistent Serial Connection Setup
try:
    ser_azimuth = serial.Serial('COM3', 9600, timeout=5)
    ser_altitude = serial.Serial('COM6', 9600, timeout=5)
    pytime.sleep(2)  # Allow time for serial connections to establish
except serial.SerialException as e:
    print(f"Error initializing serial ports: {e}")
    ser_azimuth = ser_altitude = None

import serial
import time as pytime

# Ensure all serial connections are closed if held by previous instances
def initialize_serial():
    try:
        ser_azimuth = serial.Serial('COM3', 9600, timeout=5)
        ser_altitude = serial.Serial('COM6', 9600, timeout=5)
        pytime.sleep(2)  # Allow time for serial connections to establish
        return ser_azimuth, ser_altitude
    except serial.SerialException as e:
        print(f"Error initializing serial ports: {e}")
        return None, None

ser_azimuth, ser_altitude = initialize_serial()

def send_azimuth_altitude(initial_azimuth, final_azimuth, initial_altitude, final_altitude, mode='P'):
    """
    Send azimuth and altitude angles to the Arduino for controlling motors.
    Mode: 'P' for Prediction mode, 'R' for Real-Time mode.
    """
    if not ser_azimuth or not ser_altitude:
        print("Serial ports not initialized. Cannot send data.")
        return

    try:
        # Send data to azimuth motor
        ser_azimuth.write(f"{mode}\n".encode())  # Send mode character
        pytime.sleep(0.1)
        
        if mode == 'P':
            # Prediction mode: send initial and final angles for prediction movement
            ser_azimuth.write(f"{int(initial_azimuth)}\n".encode())  # Initial azimuth angle
            pytime.sleep(0.1)  # Delay to ensure proper parsing
            ser_azimuth.write(f"{int(final_azimuth)}\n".encode())  # Final azimuth angle
        elif mode == 'R':
            # Real-Time mode: only one angle
            ser_azimuth.write(f"{int(initial_azimuth)}\n".encode())  # Target azimuth angle

        ser_azimuth.flush()
        print(f"Sent to Azimuth Motor: Mode: {mode}, Initial: {initial_azimuth}, Final: {final_azimuth if mode == 'P' else 'N/A'}")

        # Send data to altitude motor
        ser_altitude.write(f"{mode}\n".encode())  # Send mode character
        pytime.sleep(0.1)
        
        if mode == 'P':
            # Prediction mode: send initial and final angles for prediction movement
            ser_altitude.write(f"{int(initial_altitude)}\n".encode())  # Initial altitude angle
            pytime.sleep(0.1)  # Delay to ensure proper parsing
            ser_altitude.write(f"{int(final_altitude)}\n".encode())  # Final altitude angle
        elif mode == 'R':
            # Real-Time mode: only one angle
            ser_altitude.write(f"{int(initial_altitude)}\n".encode())  # Target altitude angle

        ser_altitude.flush()
        print(f"Sent to Altitude Motor: Mode: {mode}, Initial: {initial_altitude}, Final: {final_altitude if mode == 'P' else 'N/A'}")

    except serial.SerialException as e:
        print(f"Error with serial communication: {e}")

# Function to close serial ports on program exit
def close_serial_ports():
    if ser_azimuth and ser_azimuth.is_open:
        ser_azimuth.close()
    if ser_altitude and ser_altitude.is_open:
        ser_altitude.close()
    print("Serial connections closed.")

        
# Record starting and ending azimuth and altitude
def record_start_end_positions(start_azimuth, start_altitude, end_azimuth, end_altitude):
    append_text(f"Starting Position - Azimuth: {start_azimuth}°, Altitude: {start_altitude}°")
    append_text(f"Ending Position - Azimuth: {end_azimuth}°, Altitude: {end_altitude}°")

# Fetch ephemerides for the asteroid and get initial state
def fetch_asteroid_ephemerides(asteroid_name, start_date, stop_date):
    try:
        append_text(f"Fetching ephemerides for {asteroid_name}...")
        obj = Horizons(id=asteroid_name, location='500@10', epochs={'start': start_date, 'stop': stop_date, 'step': '1h'})
        ephemerides = obj.ephemerides()
        ra1, dec1, dist1 = ephemerides['RA'][0], ephemerides['DEC'][0], ephemerides['delta'][0]
        ra2, dec2, dist2 = ephemerides['RA'][1], ephemerides['DEC'][1], ephemerides['delta'][1]
        x_init, y_init, z_init = ra_dec_to_cartesian(ra1, dec1, dist1)
        delta_time = 3600  # 1 hour in seconds
        vx_init, vy_init, vz_init = calculate_velocity(ra1, dec1, dist1, ra2, dec2, dist2, delta_time)
        state_init = np.array([x_init, y_init, z_init, vx_init, vy_init, vz_init])
        append_text("Initial state fetched.")
        return state_init
    except InvalidQueryError:
        append_text(f"Error: No data found for '{asteroid_name}'.")
        return None
    except Exception as e:
        append_text(f"Error fetching ephemerides: {e}")
        return None

# Helper function for Cartesian to RA/Dec conversion
def ra_dec_to_cartesian(ra, dec, distance):
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    x = distance * np.cos(ra_rad) * np.cos(dec_rad) * AU
    y = distance * np.sin(ra_rad) * np.cos(dec_rad) * AU
    z = distance * np.sin(dec_rad) * AU
    return x, y, z

# Calculate velocity
def calculate_velocity(ra1, dec1, dist1, ra2, dec2, dist2, delta_time):
    x1, y1, z1 = ra_dec_to_cartesian(ra1, dec1, dist1)
    x2, y2, z2 = ra_dec_to_cartesian(ra2, dec2, dist2)
    vx = (x2 - x1) / delta_time
    vy = (y2 - y1) / delta_time
    vz = (z2 - z1) / delta_time
    return vx, vy, vz 

# Fetch planetary positions
def fetch_planet_positions(start_time, stop_time):
    planets = {
        'mercury': 199,
        'venus': 299,
        'earth': 399,
        'mars': 499,
        'jupiter': 599,
        'saturn': 699,
        'uranus': 799,
        'neptune': 899
    }
    planet_positions = {}
    for planet, id in planets.items():
        try:
            obj = Horizons(id=id, location='500@10', epochs={'start': start_time, 'stop': stop_time, 'step': '1d'})
            eph = obj.ephemerides()
            if 'RA' in eph.colnames and 'DEC' in eph.colnames and 'delta' in eph.colnames:
                ra, dec, dist = eph['RA'][0], eph['DEC'][0], eph['delta'][0]
                x, y, z = ra_dec_to_cartesian(ra, dec, dist)
                planet_positions[planet] = (x, y, z)
        except Exception as e:
            print(f"Error fetching data for {planet}: {e}")
    return planet_positions

def plot_results(start_time, t_span, x_values, y_values, z_values, alt_values, az_values):
    planet_positions = fetch_planet_positions(start_time.iso, (start_time + t_span[-1] * u.s).iso)

    fig = go.Figure()

    # Add asteroid's orbit
    fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', name='Asteroid Orbit'))

    # Add start and end points of the asteroid
    fig.add_trace(go.Scatter3d(x=[x_values[0]], y=[y_values[0]], z=[z_values[0]], mode='markers',
                               marker=dict(size=10, color='blue'), name='Start'))
    fig.add_trace(go.Scatter3d(x=[x_values[-1]], y=[y_values[-1]], z=[z_values[-1]], mode='markers',
                               marker=dict(size=10, color='red'), name='End'))

    # Plot planets with their accurate 3D positions
    for planet, pos in planet_positions.items():
        fig.add_trace(go.Scatter3d(x=[pos[0] / AU], y=[pos[1] / AU], z=[pos[2] / AU], mode='markers',
                                   name=planet.capitalize(), marker=dict(size=10)))

    # Plot Sun at origin
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', name='Sun', marker=dict(size=20, color='yellow')))

    # Update layout with new axis labels
    fig.update_layout(title='Asteroid Orbit and Celestial Bodies (Accurate 3D Positions)',
                      scene=dict(xaxis_title='X Coordinates (AU)',
                                 yaxis_title='Y Coordinates (AU)',
                                 zaxis_title='Z Coordinates (AU)'),
                      width=800, height=600)

    # Show the plot
    show_plot(fig)

# Function to save the plot to an HTML file and open it in the browser
def show_plot(fig):
    plot_filename = "asteroid_plot.html"
    pio.write_html(fig, file=plot_filename, auto_open=False)

    # Wait for the file to be saved before opening
    pytime.sleep(1)  # 1-second delay
    full_path = os.path.abspath(plot_filename)
    print(f"Opening plot at: {full_path}")
    webbrowser.open(f"file://{full_path}")

# Function to propagate orbit
def propagate_orbit(initial_state, t_span):
    def gravitational_acceleration(state, t):
        x, y, z, vx, vy, vz = state
        r = np.sqrt(x**2 + y**2 + z**2)
        ax = -G * M_sun * x / r**3
        ay = -G * M_sun * y / r**3
        az = -G * M_sun * z / r**3
        return [vx, vy, vz, ax, ay, az]
    return odeint(gravitational_acceleration, initial_state, t_span)

# Function to convert state (x, y, z) into Alt/Az
def convert_to_altaz(state, time):
    x, y, z = state[:3]
    observer_location = EarthLocation(lat=latitude * u.deg, lon=longitude * u.deg, height=elevation * u.m)
    altaz_time = Time(time, format='unix', scale='utc')
    sky_coord = SkyCoord(x=x * u.m, y=y * u.m, z=z * u.m, representation_type='cartesian', frame='icrs')
    altaz = sky_coord.transform_to(AltAz(obstime=altaz_time, location=observer_location))
    return altaz.az.deg, altaz.alt.deg

# Additional import for plotting functionality
import numpy as np
import astropy.units as u

# Function to collect orbital data and plot
def predict_asteroid_orbit(asteroid_name, start_date, stop_date, prediction_end_date, stop_time, end_time):
    start_time = Time(stop_date + ' ' + stop_time)
    end_time = Time(prediction_end_date + ' ' + end_time)
    total_duration = (end_time - start_time).sec

    append_text(f"Predicting celestial body orbit from {start_time.iso} to {end_time.iso}.")
    initial_state = fetch_asteroid_ephemerides(asteroid_name, start_date, stop_date)
    if initial_state is None:
        append_text("Prediction aborted due to errors.")
        return

    t_span = np.linspace(0, total_duration, 1000)
    predicted_orbit = propagate_orbit(initial_state, t_span)
    if predicted_orbit is None:
        append_text("Prediction failed.")
        return

    clear_table()

    # Lists to collect orbital data for plotting
    x_values, y_values, z_values, alt_values, az_values = [], [], [], [], []
    start_az, start_alt, end_az, end_alt = None, None, None, None

    for i, state in enumerate(predicted_orbit):
        # Collect x, y, z data
        x, y, z = state[0] / AU, state[1] / AU, state[2] / AU
        x_values.append(x)
        y_values.append(y)
        z_values.append(z)

        # Convert position to Alt/Az for plotting
        az, alt = convert_to_altaz(state, (start_time + t_span[i] * u.s).unix)
        alt_values.append(alt)
        az_values.append(az)

        # Set start and end azimuth/altitude values
        if i == 0:
            start_az, start_alt = az, alt
        if i == len(predicted_orbit) - 1:
            end_az, end_alt = az, alt

        # Insert data into the table for display
        timestamp = (start_time + t_span[i] * u.s).iso
        position_str = f"({x:.6f}, {y:.6f}, {z:.6f})"
        velocity_str = f"({state[3]:.4f}, {state[4]:.4f}, {state[5]:.4f})"
        data_table.insert('', 'end', values=(timestamp, position_str, velocity_str, f"{az:.4f}", f"{alt:.4f}"))

        progress_bar['value'] = i + 1
        root.update_idletasks()

    # Record starting and ending azimuth/altitude values
    # Inside the 'predict_asteroid_orbit' function, after record_start_end_positions call

    if start_az is not None and start_alt is not None and end_az is not None and end_alt is not None:
        # Record the starting and ending positions in the output display
        record_start_end_positions(start_az, start_alt, end_az, end_alt)

        # Send both initial and final azimuth and altitude angles to the Arduino
        send_azimuth_altitude(start_az, end_az, start_alt, end_alt, mode='P')
        
        # Append messages confirming the values sent
        append_text(f"Sent initial azimuth angle to Arduino: {start_az}")
        append_text(f"Sent final azimuth angle to Arduino: {end_az}")
        append_text(f"Sent initial altitude angle to Arduino: {start_alt}")
        append_text(f"Sent final altitude angle to Arduino: {end_alt}")

        # Plot the results
        plot_results(start_time, t_span, x_values, y_values, z_values, alt_values, az_values)


# Start the prediction process in a new thread
def start_prediction():
    asteroid_name = asteroid_entry.get()
    start_date = start_entry.get()
    stop_date = stop_entry.get()
    prediction_end_date = end_entry.get()
    stop_time = stop_time_entry.get()
    end_time = end_time_entry.get()

    if not all([asteroid_name, start_date, stop_date, prediction_end_date, stop_time, end_time]):
        messagebox.showerror("Error", "All fields must be filled out.")
        return

    threading.Thread(target=predict_asteroid_orbit, args=(asteroid_name, start_date, stop_date, prediction_end_date, stop_time, end_time)).start()

# try:
#    # ser_azimuth = serial.Serial('COM7', 9600, timeout=5)
#    # ser_altitude = serial.Serial('COM8', 9600, timeout=5)
# except serial.SerialException as e:
#     append_text(f"Error: Cannot open serial ports. {e}")

# Start prediction button
predict_button = tk.Button(input_frame, text="Start Prediction", command=start_prediction)
predict_button.pack(pady=10)

root.mainloop()
