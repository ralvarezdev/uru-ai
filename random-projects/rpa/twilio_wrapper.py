from twilio.rest import Client as TwilioClient

class Client:
    """
    A simple client class to interact with the Twilio API.
    """

    def __init__(self, account_sid: str, auth_token: str):
        """
        Initialize the Twilio client with account SID and auth token.

        Args:
            account_sid (str): The Account SID from Twilio.
            auth_token (str): The Auth Token from Twilio.
        """
        self.client = TwilioClient(account_sid, auth_token)

    def send_whatsapp_message(
        self,
        from_phone_number: str,
        to_phone_number: str,
        body: str,
        media_url: str = None
    ):
        """
        Send a WhatsApp message using Twilio API.

        Args:
            from_phone_number (str): The Twilio phone number in WhatsApp format.
            to_phone_number (str): The recipient's phone number in WhatsApp format.
            body (str): The message body to be sent.
            media_url (str, optional): The URL of the media to be sent with the message.
        """
        message = self.client.messages.create(
            from_=f"whatsapp:{from_phone_number}",
            to=f"whatsapp:{to_phone_number}",
            body=body,
            media_url=media_url if media_url else None
        )
        return message.sid