import argparse
import os
import sagemaker
from sagemaker.sklearn.model import SKLearnModel


def deploy_model(model_data, instance_type, instance_count):
    """
    Deploys a pre-trained scikit-learn model to Amazon SageMaker.
    """
    sagemaker_session = sagemaker.Session()
    role = os.getenv("SAGEMAKER_ROLE_ARN")

    # Create a SageMaker SKLearnModel object
    # The entry_point is the inference script that SageMaker will use
    # when the endpoint receives a request.
    sklearn_model = SKLearnModel(
        model_data=model_data,
        role=role,
        entry_point="inference.py",  # Your inference script
        framework_version="1.2-1",  # scikit-learn version
        sagemaker_session=sagemaker_session
    )

    # Deploy the model to a SageMaker Endpoint
    print(
        f"Deploying model to endpoint with instance type: {instance_type} and count: {instance_count}")
    predictor = sklearn_model.deploy(
        instance_type=instance_type,
        initial_instance_count=instance_count,
        endpoint_name="forest-model-endpoint"  # You can customize the endpoint name
    )

    print(f"Model deployed to endpoint: {predictor.endpoint_name}")
    return predictor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy a trained model to SageMaker.")
    parser.add_argument("--model-data", type=str, required=True,
                        help="S3 path to the trained model artifact (e.g., s3://your-bucket/model.tar.gz).")
    parser.add_argument("--instance-type", type=str, default="ml.m5.large",
                        help="SageMaker instance type for the endpoint.")
    parser.add_argument("--instance-count", type=int, default=1,
                        help="Number of instances for the SageMaker endpoint.")
    args = parser.parse_args()

    deploy_model(args.model_data, args.instance_type, args.instance_count)
