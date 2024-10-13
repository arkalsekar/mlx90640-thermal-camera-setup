from flask import Flask, jsonify, request
import json 
import random

app = Flask(__name__)

# Get Temperature for the Camera Logic
def calculate():
    return random.randint(0, 100)


@app.route("/", methods=['GET'])
def hello_world():
    data = {"camera" : "mlx90640", "data" : calculate()}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)