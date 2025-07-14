import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from .env
account_sid = os.getenv("TWILIO_ACCOUNT_SSID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_from_phone_number = os.getenv("TWILIO_FROM_PHONE_NUMBER")
twilio_to_phone_number = os.getenv("TWILIO_TO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(account_sid, auth_token)

print(f"whatsapp:{twilio_from_phone_number}")

# Send a WhatsApp message
message = client.messages.create(
    from_=f"whatsapp:{twilio_from_phone_number}",
    to=f"whatsapp:{twilio_to_phone_number}",
    body="Hello! This is a message sent via Twilio WhatsApp API."
)

# Print message SID for confirmation
print(f"Message sent with SID: {message.sid}")