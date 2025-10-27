# sagemaker-example

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
