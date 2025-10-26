import os
import yaml
import boto3
import sagemaker
from sagemaker import get_execution_role
from utils import download_model_from_s3


def deploy_model(config_path: str, env: str = "dev"):
    """
    Deploys the trained model to SageMaker.
    If endpoint exists, it updates the endpoint with a new model.
    """

    # Load config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # AWS setup
    region = config.get("region", "us-east-1")
    s3_bucket = config["s3_bucket"]
    s3_key = config.get("s3_key", "model.pkl")
    role_arn = os.environ.get("AWS_ROLE_ARN")
    if not role_arn:
        role_arn = get_execution_role()  # fallback for SageMaker notebooks

    endpoint_name = config.get("endpoint_name", f"my-model-{env}")
    model_name = f"{endpoint_name}-model"
    image_uri = config.get("image_uri")  # Docker image URI

    sagemaker_client = boto3.client("sagemaker", region_name=region)

    # Upload model to S3 if local
    local_model_path = "model.pkl"
    if os.path.exists(local_model_path):
        s3 = boto3.client("s3", region_name=region)
        s3.upload_file(local_model_path, s3_bucket, s3_key)
        print(f"Uploaded local model to s3://{s3_bucket}/{s3_key}")

    model_data_url = f"s3://{s3_bucket}/{s3_key}"

    # Check if endpoint exists
    endpoints = sagemaker_client.list_endpoints(
        NameContains=endpoint_name)["Endpoints"]
    if endpoints:
        print(f"Endpoint {endpoint_name} exists. Updating model...")
        model_name = f"{endpoint_name}-model-updated"

    # Create SageMaker model
    response = sagemaker_client.create_model(
        ModelName=model_name,
        ExecutionRoleArn=role_arn,
        PrimaryContainer={
            "Image": image_uri,
            "ModelDataUrl": model_data_url,
        },
    )
    print(f"Created model: {model_name}")

    # Create or update endpoint config
    endpoint_config_name = f"{endpoint_name}-config"
    try:
        sagemaker_client.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": "AllTraffic",
                    "ModelName": model_name,
                    "InitialInstanceCount": config.get("instance_count", 1),
                    "InstanceType": config.get("instance_type", "ml.m5.large"),
                }
            ],
        )
        print(f"Created endpoint config: {endpoint_config_name}")
    except sagemaker_client.exceptions.ResourceInUse:
        print(f"Endpoint config {endpoint_config_name} exists. Overwriting...")
        sagemaker_client.delete_endpoint_config(
            EndpointConfigName=endpoint_config_name)
        sagemaker_client.create_endpoint_config(
            EndpointConfigName=endpoint_config_name,
            ProductionVariants=[
                {
                    "VariantName": "AllTraffic",
                    "ModelName": model_name,
                    "InitialInstanceCount": config.get("instance_count", 1),
                    "InstanceType": config.get("instance_type", "ml.m5.large"),
                }
            ],
        )

    # Create or update endpoint
    try:
        sagemaker_client.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name,
        )
        print(f"Endpoint {endpoint_name} creation started...")
    except sagemaker_client.exceptions.ResourceInUse:
        print(f"Endpoint {endpoint_name} exists. Updating endpoint...")
        sagemaker_client.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name,
        )
        print(f"Endpoint {endpoint_name} update started...")

    print(f"Deployment triggered successfully for environment: {env}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True,
                        help="Path to YAML config")
    parser.add_argument("--env", type=str, default="dev",
                        help="Environment (dev/prod)")
    args = parser.parse_args()
    deploy_model(args.config, args.env)
