import pandas as pd
import joblib
import os
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

GLOBAL_MODEL_PATH = "data/global_model.pkl"
DATA_FILE = "data/sensor_data.csv"
METRICS_FILE = "data/training_metrics.csv"


def aggregate_models():
    if not os.path.exists(DATA_FILE):
        print("❌ No data available")
        return

    df = pd.read_csv(DATA_FILE)

    if len(df) < 20:
        print("⚠️ Data belum cukup untuk training")
        return

    # Label
    df['label'] = ((df['temperature'] > 85) | (df['vibration'] > 4)).astype(int)

    X = df[['temperature', 'vibration']]
    y = df['label']

    # Split data (biar bisa hitung akurasi)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Training model global
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Evaluasi
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print("\n📊 HASIL TRAINING GLOBAL")
    print(f"✅ Accuracy: {accuracy:.4f}")
    print("📄 Classification Report:")
    print(report)

    # Simpan model
    joblib.dump(model, GLOBAL_MODEL_PATH)

    # =========================
    # SIMPAN METRICS KE CSV
    # =========================
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    metrics_row = {
        "timestamp": now,
        "accuracy": accuracy
    }

    if not os.path.exists(METRICS_FILE):
        pd.DataFrame([metrics_row]).to_csv(METRICS_FILE, index=False)
    else:
        pd.DataFrame([metrics_row]).to_csv(METRICS_FILE, mode='a', header=False, index=False)

    print("💾 Metrics saved to training_metrics.csv")
    print("🌍 Global model updated!\n")