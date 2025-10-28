import joblib
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load model
model_path = os.path.join("/app/output/", "model.pkl")
model_data = joblib.load(model_path)
model = model_data["model"]


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify(status="ok")


@app.route("/invocations", methods=["POST"])
def predict():
    data = request.get_json()
    preds = model.predict(data["inputs"])
    return jsonify(predictions=preds.tolist())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
