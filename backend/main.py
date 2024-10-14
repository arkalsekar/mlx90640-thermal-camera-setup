from flask import Flask, jsonify, request
import json 
import random
import time,board,busio
import numpy as np
import adafruit_mlx90640

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate

app = Flask(__name__)

# Get Temperature for the Camera Logic

def temp():
    frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
    try:
        mlx.getFrame(frame) # read MLX temperatures into frame var
    except ValueError:
        print("Error Occuerd") # if error, just read again
    temp_celcius = np.mean(frame)
    temp_max = np.max(frame)
    temp_min = np.min(frame)
    # print(temp_min, temp_max)
    temp_ferenheit = (((9.0/5.0)*np.mean(frame))+32.0)
    return [temp_celcius, temp_ferenheit, temp_max, temp_min]


@app.route("/", methods=['GET'])
def hello_world():
    current_data = temp()
    data = {"camera" : "mlx90640", "temp_celcius" : current_data[0], "temp_ferenheit" : current_data[1], "temp_min" : current_data[2], "temp_max" : current_data[3]}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
