import argparse
import os
import yaml
import boto3
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from utils import load_data, save_model_to_s3


def train_model(config_path: str, output_dir: str):
    """
    Train a RandomForest model, save locally, and optionally upload to S3.
    """
    # Load configuration
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Load dataset
    X, y = load_data(config["data_path"])

    # Split dataset
    test_size = config.get("test_size", 0.2)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42)

    # Train model
    clf = RandomForestClassifier(
        n_estimators=config.get("n_estimators", 100),
        max_depth=config.get("max_depth", None),
        random_state=42
    )
    clf.fit(X_train, y_train)

    # Evaluate
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Test Accuracy: {acc:.4f}")

    # Save model locally
    os.makedirs(output_dir, exist_ok=True)
    local_model_path = os.path.join(output_dir, "model.pkl")
    joblib.dump(clf, local_model_path)
    print(f"Saved model to {local_model_path}")

    # Optional: Upload to S3
    if os.environ.get("ENV") == "dev":
        print("Skipping S3 upload in 'dev' environment.")
        return

    if "s3_bucket" in config and config.get("upload_to_s3", True):
        s3_bucket = config["s3_bucket"]
        s3_key = config.get("s3_key", "model.pkl")
        save_model_to_s3(local_model_path, s3_bucket, s3_key)
        print(f"Uploaded model to s3://{s3_bucket}/{s3_key}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train ML model and optionally upload to S3")
    # Use environment variables as a fallback for arguments
    default_config = os.environ.get("CONFIG_PATH")
    default_output = os.environ.get("OUTPUT_DIR", "model_output")

    parser.add_argument("--config", type=str, default=default_config, required=not default_config,
                        help="Path to config YAML file")
    parser.add_argument("--output_dir", type=str, default=default_output,
                        help="Directory to save trained model")
    args = parser.parse_args()

    train_model(args.config, args.output_dir)
