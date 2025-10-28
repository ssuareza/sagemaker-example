# sagemaker-example

This is an example how we can deploy our models in AWS Sagemaker.

For this we are using:

- **Terraform**: to create the bucket and role.

Note: The Terraform state and lock file are being saved in the repository. No S3 bucket involved.

## Usage

### Train and generate the model

```sh
dc run forest-train
```

This will create a new model and save it to `models/output/model.pkl`.

### Start endpoint

```sh
dc up forest
```

Now you can use the endpoints to make predictions. Use the `http.rest` as an example.

## Options

How you can deploy your models?

- In pods inside EKS.
- In Sagemaker using a deploy.py script.
- In Sagemaker using Terraform.
- In Sagemaker using Kubernetes Operator + Argo CD.

How you can train your models?

- Local
- GitHub Actions
- Sagemaker

How the pipeline can be?

1. User commits to `main`,
2. Train model
3. Push model image
4. Deploy model in `staging` environment
5. Deploy model in `production` environment after GitHub approval.

## SageMaker

SageMaker has a specific "contract" for custom containers:

1. Listen on port 8080.
2. Respond to `GET` requests at `/ping`.
3. Respond to `POST` requests at `/invocations` (predictions).
4. The container must be able to start running a `serve` command.

The `serve` script runs a **Gunicorn** server. Which is a robust and production-ready HTTP server. It launches multiple worker processes that can handle requests in parallel.
