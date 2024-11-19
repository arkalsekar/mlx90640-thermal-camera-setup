import time
import numpy as np
import cv2
import board
import busio
import adafruit_mlx90640
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client  # Twilio library for SMS

# Initialize I2C and the MLX90640 sensor
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)

# Set the refresh rate
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ  # Slower refresh rate for testing

# Size of the thermal image (32x24 pixels)
FRAME_WIDTH, FRAME_HEIGHT = 1280,720    #resolution for display size

# Email configuration
SENDER_EMAIL = "pranali.andhale@somaiya.edu"  # Your email address
# RECEIVER_EMAIL = "salsetteoperation@gmail.com"  # Receiver's email address
RECEIVER_EMAIL = "abdulrehmankalsekar10@gmail.com"
PASSWORD = "shqvyveewcptxdln"  # Your email app-specific password

# Twilio SMS configuration
TWILIO_PHONE = "+13164167065"  # Your Twilio phone number
TO_PHONE = "+919326383639"  # Receiver's phone number
TWILIO_SID = "ACd944e230e635174bd1270b088a8fe1f8"  # Your Twilio SID
TWILIO_AUTH_TOKEN = "5ecdff92fb1ad599e4dc61fe6835fb13"  # Your Twilio Auth Token

# Temperature threshold for sending an alert
TEMP_THRESHOLD = 40.0  # Temperature in Celsius

def send_email_alert(image_path):
    """Send an email with the processed thermal image as an attachment."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "Thermal Alert - High Temperature Detected"

    # Attach the image
    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name="thermal_image.jpg")
    msg.attach(image)

    # Send the email using SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print("Email alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_sms_alert():
    """Send an SMS alert using Twilio."""
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body="Thermal Alert: High temperature detected!",
            from_=TWILIO_PHONE,
            to=TO_PHONE
        )
        print("SMS alert sent successfully!")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def capture_thermal_data():
    frame = np.zeros((24 * 32,))  # Allocate memory for a 32x24 pixel image (768 pixels)
    try:
        mlx.getFrame(frame)  # Get thermal frame
        print("Frame captured successfully!")
        thermal_data = np.reshape(frame, (24, 32))  # Reshape into 2D array (24x32)
        return thermal_data
    except RuntimeError as e:
        print(f"Error capturing thermal data: {e}")
        return None

def process_thermal_data(thermal_data):
    # Normalize the thermal data for better visualization
    thermal_data_normalized = cv2.normalize(thermal_data, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Apply histogram equalization to improve contrast and visibility
    equalized_image = cv2.equalizeHist(thermal_data_normalized)

    # Apply a Gaussian blur to smooth out the image and reduce noise
    blurred_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)

    # Resize with Lanczos for better clarity
    resized_image = cv2.resize(blurred_image, (FRAME_WIDTH, FRAME_HEIGHT), interpolation=cv2.INTER_LANCZOS4)

    # Apply color mapping
    color_mapped_image = cv2.applyColorMap(resized_image, cv2.COLORMAP_JET)

    return color_mapped_image

# Main loop to capture and display thermal data
while True:
    thermal_data = capture_thermal_data()

    if thermal_data is not None:
        processed_image = process_thermal_data(thermal_data)
        # cv2.imshow("Thermal View", processed_image)  # Display the processed thermal image

        # Check the maximum temperature in the thermal data
        max_temp = np.max(thermal_data)
        print(f"Max Temperature: {max_temp}°C")

        # If the temperature exceeds the threshold, send an email alert and SMS alert
        if max_temp >= TEMP_THRESHOLD:
            alert_image_path = "thermal_alert_image.jpg"
            cv2.imwrite(alert_image_path, processed_image)  # Save the processed image
            send_email_alert(alert_image_path)  # Send the email alert
            send_sms_alert()  # Send the SMS alert

    # Check if 'q' is pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()  # Close the OpenCV window after loop finishes

