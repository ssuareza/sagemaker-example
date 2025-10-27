import argparse
import os
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
def model_fn(model_dir):
    """
    Loads the trained model from the disk.
    SageMaker will call this function and pass the model directory.
    """
    model_path = os.path.join(model_dir, "model.pkl")
    try:
        model = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        return None

# Load the trained model at startup
try:
    model = joblib.load(args.model)
    print(f"Model loaded successfully from {args.model}")
except FileNotFoundError:
    model = None
    print(
        f"Warning: Model file not found at {args.model}. The /invocations endpoint will not work.")

# Endpoints


@app.route("/ping", methods=["GET"])
def health():
    """Health check endpoint."""
    status = 200 if model else 404
    return jsonify({"status": "ok" if model else "model not found"}), status


@app.route("/invocations", methods=["POST"])
def invocations():
    """Prediction endpoint."""
def predict_fn(input_data, model):
    """
    Makes a prediction using the loaded model.
    """
    if not model:
        return jsonify({"error": "Model not loaded"}), 500
        raise ValueError("Model is not loaded")

    data = request.get_json()
    df = pd.DataFrame(data["instances"])
    # Assuming input_data is a dictionary with an 'instances' key
    # which is a list of records.
    df = pd.DataFrame(input_data["instances"])
    predictions = model.predict(df).tolist()
    return jsonify({"predictions": predictions})
    return {"predictions": predictions}

# Main

# The following is for local testing and is not used by SageMaker.
if __name__ == '__main__':
    # For local testing, we need a way to specify the model path.
    # We'll use an environment variable.
    model_dir = os.environ.get("SM_MODEL_DIR", ".")
    model = model_fn(model_dir)

if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/invocations', methods=['POST'])
    def invocations():
        input_data = request.get_json()
        output = predict_fn(input_data, model)
        return jsonify(output)
    
    app.run(host="0.0.0.0", port=8080)
