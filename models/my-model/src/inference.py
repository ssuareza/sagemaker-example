import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# --- Configuration ---
# Get the model path from the environment variable set in docker-compose
MODEL_DIR = os.environ.get("OUTPUT_DIR", "/app/output")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Load Model ---
# Load the trained model at startup
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    model = None
    print(
        f"Warning: Model file not found at {MODEL_PATH}. The /invocations endpoint will not work.")


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    status = 200 if model else 404
    return jsonify({"status": "ok" if model else "model not found"}), status


@app.route("/invocations", methods=["POST"])
def invocations():
    """Prediction endpoint."""
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    df = pd.DataFrame(data["instances"])
    predictions = model.predict(df).tolist()
    return jsonify({"predictions": predictions})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
