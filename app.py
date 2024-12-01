import json
import os.path

from flask import Flask
from src.controllers.datasetController import dataset_bp
from src.controllers.attentionModelController import attention_model_bp
from src.controllers.section1Controller import section1Api_bp
from src.controllers.section2Controller import section3Api_bp

app = Flask(__name__)
app.register_blueprint(dataset_bp)
app.register_blueprint(attention_model_bp)
app.register_blueprint(section1Api_bp)
app.register_blueprint(section3Api_bp)

if not os.path.exists("./logs"):
    os.makedirs("./logs")

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

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
