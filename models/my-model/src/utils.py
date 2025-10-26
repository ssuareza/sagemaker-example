import boto3
import pandas as pd


def load_data(csv_path):
    """Load dataset from CSV"""
    df = pd.read_csv(csv_path)
    X = df.drop("target", axis=1)
    y = df["target"]
    return X, y


def save_model_to_s3(local_path, bucket_name, s3_key):
    """Upload a file to S3"""
    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket_name, s3_key)


def download_model_from_s3(bucket_name, s3_key, local_path):
    """Download a file from S3"""
    s3 = boto3.client("s3")
    s3.download_file(bucket_name, s3_key, local_path)
