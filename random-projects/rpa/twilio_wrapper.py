from twilio.rest import Client as TwilioClient

class Client:
    """
    A simple client class to interact with the Twilio API.
    """

    def __init__(self, account_sid, auth_token):
        self.client = TwilioClient(account_sid, auth_token)

    def send_whatsapp_message(self, from_phone_number, to_phone_number, body):
        """
        Send a WhatsApp message using Twilio API.

        Args:
            from_phone_number (str): The Twilio phone number in WhatsApp format.
            to_phone_number (str): The recipient's phone number in WhatsApp format.
            body (str): The message body to be sent.
        """
        message = self.client.messages.create(
            from_=f"whatsapp:{from_phone_number}",
            to=f"whatsapp:{to_phone_number}",
            body=body
        )
        return message.sid