import yaml
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Load config
with open("./config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Flask App Initialization
app = Flask(__name__)

# Load the trained model at startup
try:
    model = joblib.load(config["model_path"])
    print(f"Model loaded successfully from {config['model_path']}")
except FileNotFoundError:
    model = None
    print(
        f"Warning: Model file not found at {config['model_path']}. The /invocations endpoint will not work."
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    status = 200 if model else 404
    return jsonify({"status": "ok" if model else "model not found"}), status


@app.route("/", methods=["POST"])
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
