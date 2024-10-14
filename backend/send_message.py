import os
from twilio.rest import Client
import twilio 

ACCOUNT_SID = "AC6a73f3a289cd34f507f6111cb6b0ac66"
AUTH_TOKEN = "8f7acae86319eaeb8e0cdbe338988d5d"
PHONE_NO = "+19096554220"


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ["TWILIO_ACCOUNT_SID"]
# auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(
    body="Assalamu Alaikum !! Abdul Khalik. The temperature has exeeded the limit",
    from_="+19096554220",
    # to="+919326383639",
    to="+919767771805",
)

print(message.body)