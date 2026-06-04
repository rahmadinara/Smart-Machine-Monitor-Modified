from federated.client import train_local_model
from federated.server import aggregate_models
import time

machines = ['M1', 'M2', 'M3']

while True:
    print("\n=========== 🚀 Federated Round Start ==========")

    # 1. Train di masing-masing device
    for m in machines:
        train_local_model(m)

    # 2. Aggregation di server
    aggregate_models()

    print("✅ Round selesai\n")

    time.sleep(10)