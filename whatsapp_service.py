from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()   # IMPORTANT: must be here

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = "whatsapp:+14155238886"

client = Client(
    ACCOUNT_SID,
    AUTH_TOKEN
)
def send_whatsapp_message(to, message):

    # limit for Twilio WhatsApp
    MAX_LEN = 500

    if len(message) > MAX_LEN:
        message = message[:MAX_LEN]

    client.messages.create(
        from_=FROM_NUMBER,
        to=f"whatsapp:{to}",
        body=message
    )