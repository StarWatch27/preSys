import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/api/get/<int:id>")
def testGetPath(id):
    data = {
        "id": id,
        "input1": 1
    }
    print(type(id))
    return json.dumps(data, indent=4)

@app.route("/func/get/<int:id>")
def testGetPath2(id):
    data = {
        "id": id,
        "input1": 1
    }
    print(type(id))
    return json.dumps(data, indent=4)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6006)
