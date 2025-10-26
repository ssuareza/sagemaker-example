import os
import sys

MODE = os.environ.get("MODE", "inference")
CONFIG_PATH = os.environ.get("CONFIG_PATH", "configs/dev.yaml")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/app/output")

if MODE.lower() == "train":
    from train import train_model
    train_model(config_path=CONFIG_PATH, output_dir=OUTPUT_DIR)
elif MODE.lower() == "inference":
    # Execute the Flask app. This will use the __main__ block in inference.py.
    os.execvp("python", ["python", "-m", "src.inference"])
elif MODE.lower() == "validate":
    from validate import validate_model
    validate_model(config_path=CONFIG_PATH)
else:
    print(f"Unknown MODE '{MODE}', use 'train' or 'inference'.")
    sys.exit(1)
