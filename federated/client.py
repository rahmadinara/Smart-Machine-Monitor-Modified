import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from datetime import datetime

MODEL_PATH = "data/local_model_{}.pkl"
METRICS_FILE = "data/local_metrics.csv"


def train_local_model(machine_id):
    if not os.path.exists("data/sensor_data.csv"):
        print("❌ Data tidak ditemukan")
        return None

    df = pd.read_csv("data/sensor_data.csv")

    # Filter per mesin
    df = df[df['machine_id'] == machine_id]

    if len(df) < 10:
        print(f"⚠️ Data {machine_id} belum cukup")
        return None

    # Label
    df['label'] = ((df['temperature'] > 85) | (df['vibration'] > 4)).astype(int)

    X = df[['temperature', 'vibration']]
    y = df['label']

    # Split untuk evaluasi
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Training
    model = RandomForestClassifier(n_estimators=20, random_state=42)
    model.fit(X_train, y_train)

    # Evaluasi
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n📊 LOCAL TRAINING RESULT ({machine_id})")
    print(f"✅ Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, y_pred))

    # Simpan model
    path = MODEL_PATH.format(machine_id)
    joblib.dump(model, path)

    # =========================
    # SIMPAN METRICS
    # =========================
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    metrics_row = {
        "timestamp": now,
        "machine_id": machine_id,
        "accuracy": accuracy
    }

    if not os.path.exists(METRICS_FILE):
        pd.DataFrame([metrics_row]).to_csv(METRICS_FILE, index=False)
    else:
        pd.DataFrame([metrics_row]).to_csv(METRICS_FILE, mode='a', header=False, index=False)

    print(f"💾 Local metrics saved ({machine_id})")

    return path