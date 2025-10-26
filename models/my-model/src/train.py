import argparse
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train_model(sample_path, output_dir):
    """
    Train a RandomForest model, save locally, and optionally upload to S3.
    """

    # Load dataset
    X, y = load_data(sample_path)

    # Split dataset
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # Train model
    clf = RandomForestClassifier(
        n_estimators=100, max_depth=5, random_state=42)
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


def load_data(csv_path):
    """Load dataset from CSV"""
    df = pd.read_csv(csv_path)
    X = df.drop("target", axis=1)
    y = df["target"]
    return X, y


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a RandomForest model.")
    parser.add_argument("--sample", type=str, required=True,
                        help="Path to the input CSV sample.")
    parser.add_argument("--output", type=str, required=True,
                        help="Directory to save the trained model.")
    args = parser.parse_args()

    train_model(args.sample, args.output)
