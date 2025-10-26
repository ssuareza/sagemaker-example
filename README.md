# sagemaker-example

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
