# sagemaker-example

Create a Monorepository with the following requirements:

1. This repository will deploy models in AWS Sagemaker.
2. We use Terraform to build the underline infrastructure.
3. The model should be able to run locally with Docker.
4. The model should include a Github Action pipeline that includes: train.yaml (trains the model and push the file to AWS s3) and deploy.yaml (deploys the model to AWS sagemaker and creates an endpoint)
5. We will have two environments, dev and production (production can be the main branch of the repository).  

## Usage

### Train the model and save it

```sh
dc run my-model-train
```

This will create a new model and save it to `models/output/model.pkl`.

### Start endpoint

```sh
dc up my-model
```

Now you can use the endpoints to make predictions. Use the `http.rest` as an example.
