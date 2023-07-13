import csv
import sys
import serial
import time

# Initialize the position of each sensor
sensor_positions = {
    'r_A1': (8, 3),
    'r_A2': (6, 3),
    'r_A3': (3, 6)
}

# Initialize distance data for each sensor
sensor_distances = {
    'r_A1': None,
    'r_A2': None,
    'r_A3': None
}

# Create a serial object to read data from the Serial Monitor
ser = serial.Serial('COM3', 115200)

# Create a list to store the x, y, and timestamp data
positions = []

try:
    while True:
        try:
            data = ser.readline().decode('ascii').strip()
            address, range_value = data.split()
            address = int(address)
            range_value = float(range_value)

            # Update distance data for each sensor
            if address == 1781:
                sensor_distances['r_A1'] = range_value
            elif address == 1782:
                sensor_distances['r_A2'] = range_value
            elif address == 1783:
                sensor_distances['r_A3'] = range_value

            # Perform trilateration when distance data is available for all sensors
            if all(sensor_distances.values()):
                r1 = sensor_distances['r_A1']
                r2 = sensor_distances['r_A2']
                r3 = sensor_distances['r_A3']
                x1, y1 = sensor_positions['r_A1']
                x2, y2 = sensor_positions['r_A2']
                x3, y3 = sensor_positions['r_A3']

                A = 2 * x2 - 2 * x1
                B = 2 * y2 - 2 * y1
                C = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
                D = 2 * x3 - 2 * x2
                E = 2 * y3 - 2 * y2
                F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

                x = (C * E - F * B) / (E * A - B * D)
                y = (C * D - A * F) / (B * D - A * E)

                # Round the position values to 2 decimal places
                x_rounded = round(x, 2)
                y_rounded = round(y, 2)

                # Get the current timestamp
                timestamp = time.time()

                # Print the object position and timestamp
                print(f"Object position: ({x_rounded}, {y_rounded}), Timestamp: {timestamp}")

                # Add the x, y, and timestamp data to the list
                positions.append([x_rounded, y_rounded, timestamp])

        except ValueError:
            pass

except KeyboardInterrupt:
    # Save the positions data to a CSV file
    with open('trilateration_visual.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Y', 'Timestamp'])  # Write header row
        writer.writerows(positions)  # Write the data rows
