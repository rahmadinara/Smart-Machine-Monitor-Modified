import time
import random
import csv
import os
from predictor import predict_health
from db_handler import insert_log

DATA_FILE = 'data/sensor_data.csv'

def simulate_5g_network_delay():
    delay = random.uniform(0.001, 0.05)
    time.sleep(delay)
    return delay

def stream_data():
    print("🔄 Starting 5G network simulator...")
    last_line = 0

    while True:
        if not os.path.exists(DATA_FILE):
            time.sleep(2)
            continue

        with open(DATA_FILE, 'r') as file:
            lines = file.readlines()

        # Ambil baris data baru
        new_data = lines[last_line + 1:]

        for row in new_data:
            fields = row.strip().split(',')
            if len(fields) != 4:
                continue  # Skip jika baris tidak lengkap

            timestamp, machine_id, temperature, vibration = fields

            delay = simulate_5g_network_delay()
            
            # Prediksi status kesehatan menggunakan fungsi pkl/fallback
            prediction = predict_health(fields)

            # Insert ke SQLite
            insert_log(timestamp, machine_id, float(temperature), float(vibration), prediction)

            status_str = '⚠️ At Risk' if prediction == 1 else '✅ Healthy'
            print(f"[{timestamp}] 5G Delay: {round(delay * 1000, 2)} ms → {machine_id}: {status_str} (T:{temperature}°C, V:{vibration}m/s²)")

        last_line = len(lines) - 1
        time.sleep(1)

if __name__ == "__main__":
    stream_data()