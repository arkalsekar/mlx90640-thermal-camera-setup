# MLX90640 Thermal Camera Setup with Raspberry Pi 4
This is MLX90640 Thermal Camera Setup created using MLX90640 Thermal Camera from waveshare and raspberry pi 4 along with sunfounders LCD screen create for Tata Power Plant for Monitoring Temperatures of Capacitor Banks

## Setup 
The Setup includes the following tasks

1. Enable I2C and SPI from Raspberry Home > Raspberry pi Configuration > Interfaces > Enable SPI and I2C and reboot

2. Pinout of MLX90640 
The MLX90640 Thermal Camera has 4 pins that need to be connected to the controller and currently supports the Raspberry Pi, STM32F405R, and ESP32 series.

* VCC: Power supply pin, should be connected to the control 3.3V or 5V power supply.
* GND: Ground pin, corresponds to the connection of the ground (GND).
* SDA: Data pin for I2C communication, connected to the GPIO of the controller.
* SCL: Clock pin for I2C communication, connected to the GPIO of the controller
Certain variants of the MLX90640 thermal camera module are equipped to support the UART communication protocol in addition to the standard I2C interface. This feature allows for greater flexibility in integrating the sensor with a wider range of microcontrollers and systems that might prefer UART for simplicity or specific application requirements.

3. Update the Raspberry PI 
```bash 
sudo apt-get update
sudo apt-get upgrade
```

4. Add the following lines in config.txt
```bash
sudo nano /bin/firmware/config.txt
```
Add these line ```dtparam=i2c_arm=on, i2c_arm_baudrate=400000``` as shown in the figure 

5. Set Static IP for Raspberry PI (Optional For Now)
```
In Bookworm:
- click the network icon
- advanced
- edit connections
- wired
- set the IP under the IPv4 tab
(at least thats what worked for me)
```
Refer this for more details https://forums.raspberrypi.com/viewtopic.php?t=357678

6. Create a Virtual Environment 
```bash
cd Desktop
python -m venv myenv
```

Activate the environment 
```bash
source bin/activate
```

5. Download this complete repository in the myenv directory as a zip and unzip it using 
```bash 
unzip -d mlx90640-thermal-camera-setup-main.zip . 
```

6. Install the Requirements Before Installation make sure you have activated the environment using ```source bin/activate```
```python 
pip install -r requirements.txt
```

7. Install the following packages on the system ie in New Terminal 
```bash
sudo apt-get install -y i2c-tools
 
```
## How to run the setup 
1. In order to get the feed on the raspberry pi lcd screen run the ```thermal_real_feed.py``` script
```python
python thermal_real_feed.py 
``` 

2. Create a Server, run the main script from backend folder
```python 
python main.py
```

3. Access the Frontend on the Remote Laptop connected with the same network
```python 
open the index.html file on the remote laptop
```
