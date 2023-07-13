import math
import serial

# Inisialisasi posisi masing-masing sensor
posisi_sensor = {
    'r_A1': (3, 1),
    'r_A2': (6, 1),
    'r_A3': (9, 2),
    'r_A4': (12, 3)
}

# Inisialisasi data jarak untuk masing-masing sensor
jarak_sensor = {
    'r_A1': None,
    'r_A2': None,
    'r_A3': None,
    'r_A4': None
}

# Membuat objek Serial untuk membaca data dari Serial Monitor
ser = serial.Serial('COM3', 115200)

while True:
    try:
        data = ser.readline().decode('ascii').strip()
        address, range_value = data.split()
        address = int(address)
        range_value = float(range_value)
        
        # Mengisi data jarak untuk setiap sensor
        if address == 1781:
            jarak_sensor['r_A1'] = range_value
        elif address == 1782:
            jarak_sensor['r_A2'] = range_value
        elif address == 1783:
            jarak_sensor['r_A3'] = range_value
        elif address == 1784:
            jarak_sensor['r_A4'] = range_value
            
        # Jika sudah ada data jarak untuk keempat sensor, lakukan trilaterasi
        if all(jarak_sensor.values()):
            r1 = jarak_sensor['r_A1']
            r2 = jarak_sensor['r_A2']
            r3 = jarak_sensor['r_A3']
            r4 = jarak_sensor['r_A4']
            x1, y1 = posisi_sensor['r_A1']
            x2, y2 = posisi_sensor['r_A2']
            x3, y3 = posisi_sensor['r_A3']
            x4, y4 = posisi_sensor['r_A4']
            
            A = 2 * x2 - 2 * x1
            B = 2 * y2 - 2 * y1
            C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
            D = 2 * x3 - 2 * x2
            E = 2 * y3 - 2 * y2
            F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
            G = 2 * x4 - 2 * x3
            H = 2 * y4 - 2 * y3
            I = r3**2 - r4**2 - x3**2 + x4**2 - y3**2 + y4**2
            
            x = (C * E - F * B) / (E * A - B * D)
            y = (C * D - A * F) / (B * D - A * E)

            # Menampilkan hasil posisi objek
            print(f"Posisi objek: ({x:.2f}, {y:.2f})")
            
    except ValueError:
        pass
