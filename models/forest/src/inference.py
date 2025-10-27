import argparse
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Flask App Initialization
app = Flask(__name__)

# Parse command-line arguments
parser = argparse.ArgumentParser(
    description="Start a Flask API with a trained model.")
parser.add_argument("--model", type=str, required=True,
                    help="Path to the trained model file.")
args = parser.parse_args()

# Load the trained model at startup
try:
    model = joblib.load(args.model)
    print(f"Model loaded successfully from {args.model}")
except FileNotFoundError:
    model = None
    print(
        f"Warning: Model file not found at {args.model}. The /invocations endpoint will not work.")


@app.route("/ping", methods=["GET"])
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
