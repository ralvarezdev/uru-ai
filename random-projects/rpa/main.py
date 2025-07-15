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
    pdf_link = upload_to_gofile(SALES_REPORT_PDF)

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send a WhatsApp message
    message = client.send_whatsapp_message(
        twilio_from_phone_number,
        twilio_to_phone_number,
        "Hola, el reporte de ventas ha sido generado y está disponible en el siguiente enlace: " + pdf_link,
        media_url=pdf_link
    )

