# sagemaker-example

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
