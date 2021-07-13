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
- flask
- falcon
- fastAPI

## Flask
Flask is my favorite and the most popular framework to make such things.
The code is very simple.
```python 
from flask import Flask, request, jsonify
from model import predict as model_predict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    numbers = request.json
    message = {"prediction": model_predict(numbers)}
    print(message)
    return jsonify(message)

if __name__ == '__main__':
    app.run()
```

To run server type next command in shell
`python flask_app.py`

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626074814739/nudnMedvU.png)

Our service takes a list of numbers in json format and returns prediction.
To test our service we could use programs like  [postman](https://www.postman.com/), but we'd better write the client ourselves.

```python
import requests

def send_test():
    r = requests.post("http://localhost:5000/predict", json=[1, 2, 3, 4.44])
    print(r.status_code)
    print(r.text)

if __name__ == '__main__':
    send_test()
```

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626075068193/dwu_6H7Zv.png)

## Falcon

Falcon framework doesn't include his own development server. And additional we have to install some wsgi server with them. I use `waitress`, because it's easy to install on the windows platform.
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

For me, this code seems more sophisticated, and I don't like it. But it works fine and you can use this template too.
To run this script just type 'python falcon_app.py' in the console.

## FastAPI

The young and trending framework. Just look how clean this code is.
```python
from typing import List
from fastapi import FastAPI
from model import predict as model_predict

app = FastAPI()

@app.post("/predict")
async def predict(numbers: List[float]):
    message = {"prediction": model_predict(numbers)}
    print(message)
    return message
```

It's only just one function. I really like it.  
But there are also disadvantages. For starting the script, you need to install ASGI server. And you will need to run the server via command line.
As ASGI server I choose  [uvicorn](https://www.uvicorn.org/).  
To run the script you need to run next command:  
`uvicorn fast_api_app:app --port 5000 --reload`


![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626155205335/B-yT_oicI.png)

Works, just fine! But it has some warnings in it. Never mind, this is because I use different versions of sklearn library in the training step, and in production. Don't ever do that in real projects.

## Bonus 1. Let's wrap it in a container

Let's create docker container for our script.
```docker
FROM python:3.9

RUN apt-get update -y && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN pip install --upgrade pip
RUN pip install uwsgi flask sklearn numpy

WORKDIR /app
COPY src /app

CMD ["uwsgi", "--http", ":5000", "--module", "flask_app:app", "--processes", "4", "--master"]
```

## Bonus 2. Let's add out script to nginx docker image.

```docker
FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install sklearn numpy

WORKDIR /app
COPY src /app

ENV LISTEN_PORT 5000

RUN mv /app/flask_app.py /app/main.py

```