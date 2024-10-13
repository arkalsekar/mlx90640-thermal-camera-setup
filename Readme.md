## MLX90640 Thermal Camera Setup with Raspberry Pi 4
This is MLX90640 Thermal Camera Setup created using MLX90640 Thermal Camera from waveshare and raspberry pi 4 along with sunfounders lcd screen

# Setup 
The Setup includes the following tasks

1. Enable I2C and SPI from Raspberry Home > Raspberry pi Configuration > Interfaces > Enable SPI and I2C and reboot

2. Add the following lines in config.txt
```bash
sudo nano /bin/firmware/config.txt

```

3. Set Static IP for Raspberry PI

4. Create a Virtual Environment 
```bash
cd Desktop
python -m venv myenv
```
Activate the environment 
```bash
source bin/activate
```

5. Download this complete repository as a zip and unzip it using 
'''bash 
unzip 
'''

6. Install the Requirements
```python 
pip install -r requirements.txt
```

# How to run the setup 
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