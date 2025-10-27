import argparse
import os
from sagemaker import Session
from sagemaker.sklearn.model import SKLearnModel


def deploy_model(model_data, instance_type, instance_count, role_arn):
    """
    Deploys a pre-trained scikit-learn model to Amazon SageMaker.
    """
    # Create session
    session = Session()

    # Get the directory of the current script to use as source_dir
    script_path = os.path.dirname(os.path.realpath(__file__))

    # Create a SageMaker SKLearnModel object
    sklearn_model = SKLearnModel(
        model_data=model_data,
        role=role_arn,
        entry_point="inference.py",
        source_dir=script_path,
        framework_version="1.2-1",
        sagemaker_session=session
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
    parser.add_argument("--role-arn", type=str, required=True,
                        help="The AWS IAM role ARN for SageMaker to assume.")
    parser.add_argument("--instance-type", type=str, default="ml.m5.large",
                        help="SageMaker instance type for the endpoint.")
    parser.add_argument("--instance-count", type=int, default=1,
                        help="Number of instances for the SageMaker endpoint.")
    args = parser.parse_args()

    deploy_model(args.model_data, args.instance_type,
                 args.instance_count, args.role_arn)
