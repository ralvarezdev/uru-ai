import os
from dotenv import load_dotenv

from twilio_wrapper import Client

from analyzer import analyze_sales_data
from summary import generate_summary, generate_pdf
from gofile_io import upload_to_gofile
from constants import (
    SALES_REPORT_PDF,
)

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()

    # Twilio credentials from .env
    account_sid = os.getenv("TWILIO_ACCOUNT_SSID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_from_phone_number = os.getenv("TWILIO_FROM_PHONE_NUMBER")
    twilio_to_phone_number = os.getenv("TWILIO_TO_PHONE_NUMBER")
    proxy_server_url = os.getenv("PROXY_SERVER_URL")

    # Generate PDF report
    (segment_counts, top_counts, numerical_stats, anual_summary,
     quarterly_summary) = analyze_sales_data()

    summary = generate_summary(
        segment_counts,
        top_counts,
        numerical_stats,
        anual_summary,
        quarterly_summary
    )
    generate_pdf("sales_report.pdf", summary)

    # Upload the PDF to GoFile.io
    page_link, direct_link = upload_to_gofile(SALES_REPORT_PDF)

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Generate the proxy URL for the PDF
    proxy_url = f"{proxy_server_url}/proxy?url={direct_link}"

    # Send a WhatsApp message
    message = client.send_whatsapp_message(
        twilio_from_phone_number,
        twilio_to_phone_number,
        "¡Hola!, el reporte de ventas ha sido generado y está disponible en "
        "el siguiente enlace: " + page_link,
        media_url=proxy_url
    )
