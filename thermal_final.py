import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage
import os
from twilio.rest import Client
import twilio 
from datetime import datetime

# Tokens for TWilio acount
ACCOUNT_SID = "AC6a73f3a289cd34f507f6111cb6b0ac66"
AUTH_TOKEN = "8f7acae86319eaeb8e0cdbe338988d5d"
PHONE_NO = "+19096554220"


def send_message(temp):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body="Assalamu Alaikum !! Abdul Khalik. The temperature has exeeded the limit, current temp is " + str(temp),
        from_="+19096554220",
        to="+919326383639",
        # to="+919767771805",
    )


last_time = datetime.now()

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate
mlx_shape = (24,32) # mlx90640 shape

mlx_interp_val = 10 # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0]*mlx_interp_val,
                    mlx_shape[1]*mlx_interp_val) # new shape

fig = plt.figure(figsize=(12,9)) # start figure
ax = fig.add_subplot(111) # add subplot
fig.subplots_adjust(0.05,0.05,0.95,0.95) # get rid of unnecessary padding
therm1 = ax.imshow(np.zeros(mlx_interp_shape),interpolation='none',
                   cmap=plt.cm.bwr,vmin=25,vmax=45) # preemptive image
cbar = fig.colorbar(therm1) # setup colorbar
cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

fig.canvas.draw() # draw figure to copy background
ax_background = fig.canvas.copy_from_bbox(ax.bbox) # copy background
fig.show() # show the figure before blitting

frame = np.zeros(mlx_shape[0]*mlx_shape[1]) # 768 pts
def plot_update():
    fig.canvas.restore_region(ax_background) # restore background
    mlx.getFrame(frame) # read mlx90640
    data_array = np.fliplr(np.reshape(frame,mlx_shape)) # reshape, flip data
    data_array = ndimage.zoom(data_array,mlx_interp_val) # interpolate
    therm1.set_array(data_array) # set data
    therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
    # cbar.on_mappable_changed(therm1) # update colorbar range
    plt.draw()
    # print(np.max(data_array))
    ax.draw_artist(therm1) # draw new thermal image
    fig.canvas.blit(ax.bbox) # draw background
    fig.canvas.flush_events() # show the new image
    return data_array

t_array = []
while True:
    t1 = time.monotonic() # for determining frame rate
    try:
        temp = plot_update() # update plot
        print(np.max(temp))
    except:
        continue
    # approximating frame rate
    t_array.append(time.monotonic()-t1)
    if np.max(temp) > 37:
        current_time = datetime.now()
        time_diff = current_time - last_time
        time_diff_sec = time_diff.total_seconds()
        last_time = current_time
        if (time_diff_sec > 5):
            send_message(37)
        print("Temperature Exeeded and time difference is " + str(time_diff_sec))

    if len(t_array)>10:
        t_array = t_array[1:] # recent times for frame rate approx
    print('Frame Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
