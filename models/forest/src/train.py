import pandas as pd
import joblib
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def train(sample, output):
    # Load CSV
    df = pd.read_csv(sample)

    # Replace 'target' with your actual label column
    X = df.drop("target", axis=1)
    y = df["target"]

    # Keep feature names consistent
    feature_names = X.columns.tolist()

    # Split into train/test (optional, can skip for full training)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Train RandomForest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Optional: evaluate
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Validation Accuracy: {acc:.4f}")

    # Save model
    model_path = output
    joblib.dump({"model": clf, "feature_names": feature_names}, model_path)
    print(f"Model saved to {model_path}")


# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a RandomForest model.")
    parser.add_argument("--sample", type=str, required=True,
                        help="Path to the input CSV sample.")
    parser.add_argument("--output", type=str, required=True,
                        help="Directory to save the trained model.")
    args = parser.parse_args()

    train(args.sample, args.output)
