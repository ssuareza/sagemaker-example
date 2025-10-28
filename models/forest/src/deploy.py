import argparse
import sagemaker


def deploy_model(instance_type, instance_count, role_arn, image_uri):
    """
    Deploy a SageMaker endpoint using a custom container.

    Args:
        instance_type (str): SageMaker instance type.
        instance_count (int): Number of instances.
        role_arn (str): SageMaker IAM role ARN.
        image_uri (str): ECR URI of the custom container.

    Returns:
        predictor: SageMaker Predictor object
    """
    session = sagemaker.Session()

    # Create SageMaker model from custom container
    model = sagemaker.model.Model(
        image_uri=image_uri,
        role=role_arn,
        sagemaker_session=session
    )

    # Deploy endpoint
    predictor = model.deploy(
        initial_instance_count=instance_count,
        instance_type=instance_type
    )

    if predictor:
        print(f"Endpoint deployed successfully: {predictor.endpoint_name}")
        return predictor
    else:
        print(
            "Endpoint deployment started asynchronously or failed. No predictor returned.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy a custom Docker container to SageMaker."
    )
    parser.add_argument("--role-arn", type=str, required=True,
                        help="The AWS IAM role ARN for SageMaker to assume.")
    parser.add_argument("--instance-type", type=str, default="ml.m5.large",
                        help="SageMaker instance type for the endpoint.")
    parser.add_argument("--instance-count", type=int, default=1,
                        help="Number of instances for the SageMaker endpoint.")
    parser.add_argument("--image-uri", type=str, required=True,
                        help="ECR URI of the custom Docker container.")

    args = parser.parse_args()

    deploy_model(
        instance_type=args.instance_type,
        instance_count=args.instance_count,
        role_arn=args.role_arn,
        image_uri=args.image_uri
    )
