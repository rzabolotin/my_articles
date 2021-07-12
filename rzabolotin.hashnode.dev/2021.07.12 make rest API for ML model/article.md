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
