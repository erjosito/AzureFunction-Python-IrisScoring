# Python Function to score a previously trained ML model

This function loads a previously trained machine learning model (in this particular case using sklearn and Azure ML Service) and scores it with data supplied over POST calls. You can look at it as the hello world of ML scoring.

The Azure ML Service supports deployment of registered models to a variety of target compute platforms, but at this point in time Azure Functions is not one of them. It is fairly easy though training a model, exporting it using joblib (I am using here joblib instead of pickle because it tends to work better for sklearn models), and package it next to the function.

The source code of this function includes an `irismodel.pkl` file that contains a model previously trained with the iris dataset.

## Deplo to Azure

You can deploy Azure Functions in multiple ways, here what I would consider to be the simplest

1. Fork and clone this repo to your computer
2. Open with with Visual Studio (make sure you fulfill [these prerequisites](https://docs.microsoft.com/en-us/azure/azure-functions/tutorial-vs-code-serverless-python#prerequisites)})
3. Deploy using [these instructions](https://docs.microsoft.com/en-us/azure/azure-functions/tutorial-vs-code-serverless-python#deploy-to-azure-functions)

## Configuration

Please follow these steps depending on whether you want a hello world experience or using it with your own model:

### Option 1. To use the provided model (easiest)

* Deploy this function, and score it sending for example this JSON payload (one example of each class is provided here, so the prediction result should look like `[0, 1, 2]`):

```json
{
	"data": [
		[ "5.1", "3.5", "1.4", "0.2" ],
		["7.0", "3.2", "4.7", "1.4"],
		["6.3", "3.3", "6.0", "2.5"]
	]
}
```

The answer should look like this:

```json
{
  "operation_result": "success",
  "data": "[['5.1', '3.5', '1.4', '0.2'], ['7.0', '3.2', '4.7', '1.4'], ['6.3', '3.3', '6.0', '2.5']]",
  "prediction": "[0, 1, 2]"
}
```

### Option 2. Change to use with your own model (harder)

If you decide to move over the hello world stage, you might want to follow these steps to deploy with your own model:

* Train a ML model as you prefer. You can use for example [this tutorial for training a model with sklearn and the Azure ML Service](https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/machine-learning/service/how-to-train-scikit-learn.md)
* Create a Python HTTP-triggered Azure Function. You can follow [this tutorial](https://docs.microsoft.com/azure/azure-functions/functions-create-first-function-python)
* Include the serialized model (.pkl file) in your function directory, modify your code at will
* Send HTTP Post calls. The exact format of the body will depend on how you trained your model.

## Application settings

No application settings required.

## Running Locally

Visual Studio function app project is included.