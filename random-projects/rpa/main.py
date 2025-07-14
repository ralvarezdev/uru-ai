import os
from dotenv import load_dotenv

from twilio_wrapper import Client

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Twilio credentials from .env
    account_sid = os.getenv("TWILIO_ACCOUNT_SSID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_from_phone_number = os.getenv("TWILIO_FROM_PHONE_NUMBER")
    twilio_to_phone_number = os.getenv("TWILIO_TO_PHONE_NUMBER")

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send a WhatsApp message
    message = client.send_whatsapp_message(
        twilio_from_phone_number,
        twilio_to_phone_number,
        "Hello! This is a message sent via Twilio WhatsApp API."
    )