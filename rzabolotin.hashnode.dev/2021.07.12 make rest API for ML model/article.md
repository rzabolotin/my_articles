## Introduction
Hi, friends! Nice to see you again. Now I've installed Grammarly as a chrome extension, so I hope to have fewer misspellings. It really helps.

Today I want to share with you some basic templates, how to make a service from your ML model. 

First off, I show my simple model.
Here it is.
```python
import pickle
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

model = Pipeline(
            [
                ("scaling",StandardScaler()),
                ("logistic", LogisticRegression())
            ]
)
X,y = load_iris(return_X_y=True)
model.fit(X,y)

with open("pickled_model.pkl", "wb") as f_pkl:
    pickle.dump(model, f_pkl)
```

Let's write some code to simplify the usage of the model.
```python
import pickle
import numpy as np
from typing import List

MODEL_FILE = "pickled_model.pkl"
model = pickle.load(open(MODEL_FILE, "rb"))

def predict(numbers: List[float]):
    x = np.array(numbers).reshape(1, -1)
    return int(model.predict(x))
```

Ok, we have pickled model, and also a function that makes predictions, using it.
Now we'll create REST API services for it. I show you examples in three popular frameworks:
- Flask
- Falcon
- FastAPI
For some reason they all start with the letter **F**

## Flask
Flask is my favorite and the most popular framework to make such things.
The code is very simple.
```python 
from flask import Flask, request, jsonify
from loguru import logger
from model import predict as model_predict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    numbers = request.json
    logger.info(f"Got request for prediction {numbers}")
    prediction = model_predict(numbers)
    logger.success(f"Calculated the prediction = {prediction}")
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run()
```

To run server type next command in shell
`python flask_app.py`


![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626229239340/WGq5s5JJTa.png)

Our service takes a list of numbers in json format and returns prediction.
To test our service we could use programs like  [postman](https://www.postman.com/), but we'd better write the client ourselves.

```python
import requests
from loguru import logger

def send_test():
    logger.debug("Sending post request to local server")
    r = requests.post("http://localhost:5000/predict", json=[1, 2, 3, 4.44])
    r.raise_for_status()
    logger.debug(f"Got response status code: {r.status_code}")
    logger.info(f"Got answer from server: {r.text}")

if __name__ == '__main__':
    send_test()
```
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626229490411/O46KRHbUo.png)
## Falcon

Falcon framework doesn't include his own development server. That's why, we have to install some wsgi server with them. I use  [waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/)  because it's easy to install on the windows platform.
```python
import falcon
from waitress import serve
from model import predict as model_predict

class PredictHandler:
    def on_post(self, req, resp):
        numbers = req.get_media()
        message = {"prediction": model_predict(numbers)}
        print(message)
        resp.media = message

app = falcon.App()
app.add_route('/predict', PredictHandler())

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=5000)
```

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626229819256/DLxxIDFay.png)
For me, this code seems more sophisticated, and I don't like it. But it works fine and you can use this template too.
To run this script just type 'python falcon_app.py' in the console.

## FastAPI

The young and trending framework. Just look how clean this code is.
```python
from typing import List
from fastapi import FastAPI
from loguru import logger
from model import predict as model_predict

app = FastAPI()

@app.post("/predict")
async def predict(numbers: List[float]):
    logger.info(f"Got request for prediction {numbers}")
    prediction = model_predict(numbers)
    logger.success(f"Calculated the prediction = {prediction}")
    return {"prediction": prediction}

```

It's only just one function. I definitely like it.  
But there are also disadvantages. For starting the script, you need to install ASGI server. And you will need to run the server via command line.
As ASGI server I choose  [uvicorn](https://www.uvicorn.org/).  
To run the script you need to run next command:  
`uvicorn fast_api_app:app --port 5000 --reload`

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626230087847/HKSe3pybB.png)

Works, just fine! 

## At the end
Python is known for having [many web frameworks](https://wiki.python.org/moin/WebFrameworks), and anyone can find the one they like best. I have shown examples of the implementation of the simplest API on three of them.   



The code of examples are available on [github](https://github.com/rzabolotin/simple_rest_api)


Hope you found it interesting. See you.
