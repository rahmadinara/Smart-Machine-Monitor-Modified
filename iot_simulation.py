import csv
import random
import time
from datetime import datetime
import os

DATA_FILE = 'data/sensor_data.csv'

if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.isfile(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'machine_id', 'temperature', 'vibration'])

def generate_sensor_data():
    print("🚀 IoT Simulator Running... Pres Ctrl+C to stop.")
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        machine_id = random.choice(['M1', 'M2', 'M3'])

        # Variasikan suhu dan getaran agar ada data aman dan data anomali
        temperature = round(random.uniform(55, 95), 2)
        vibration = round(random.uniform(1.0, 5.0), 2)

        data = [timestamp, machine_id, temperature, vibration]

        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

        print(f"📡 Generated IoT Data: {data}")
        time.sleep(2)

if __name__ == "__main__":
    generate_sensor_data()