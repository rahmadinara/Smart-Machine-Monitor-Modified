import joblib
import os
import warnings

# Sembunyikan warning sklearn
warnings.filterwarnings("ignore", category=UserWarning)

MODEL_FILE = 'data/global_model.pkl'

# Cache model biar tidak load berulang
model = None

def load_model():
    global model
    if model is None:
        if os.path.exists(MODEL_FILE):
            model = joblib.load(MODEL_FILE)
            print("✅ Global model loaded")
        else:
            print("⚠️ Global model belum ada, pakai heuristic")
    return model


def predict_health(sensor_row):
    try:
        temperature = float(sensor_row[2])
        vibration = float(sensor_row[3])

        # Load model sekali saja
        mdl = load_model()

        # =========================
        # 1. PREDIKSI DENGAN MODEL
        # =========================
        if mdl is not None:
            features = [[temperature, vibration]]
            prediction = int(mdl.predict(features)[0])
            return prediction

        # =========================
        # 2. FALLBACK HEURISTIC
        # =========================
        else:
            return 1 if (temperature > 85.0 or vibration > 4.0) else 0

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return 0