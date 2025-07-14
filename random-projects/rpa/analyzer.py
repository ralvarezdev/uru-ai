import os

from fpdf import FPDF
import pandas as pd

from constants import SALES_XLSX, DATA_DIR

# Load the Excel file
data = pd.read_excel(SALES_XLSX, engine="openpyxl")

# Count the number of appearances of each data in the 'Segmento' column
segment_counts = data['Segmento'].value_counts()

# Count the number of appearances of each data in the different columns that are not binary or numerical.
columns_counts = {}
for column in ['Canal', 'Cliente', 'Fecha', 'Sede', 'Vendedor']:
    # Count the occurrences of each unique value in the column
    counts = data[column].value_counts()
    columns_counts[column] = counts

# Get the top 5 most common values for each column
top_counts = {}
for column, counts in columns_counts.items():
    top_counts[column] = counts.head(5)

def generate_summary():
    """
    Function to generate a summary of the sales data.
    """
    summary = {
        "Ventas por segmento": segment_counts.to_dict(),
        "Top 5 Canales con mayor cantidad de ventas": top_counts[
            'Canal'].to_dict(),
        "Top 5 Clientes con más compras": top_counts['Cliente'].to_dict(),
        "Top 5 Fechas donde se realizaron más ventas": top_counts[
            'Fecha'].to_dict(),
        "Top 5 Sedes con mayor cantidad de ventas": top_counts[
            'Sede'].to_dict(),
        "Top 5 Vendedores con más ventas realizadas": top_counts[
            'Vendedor'].to_dict()
    }

    return summary

def generate_pdf(file_name: str, summary: dict):
    """
    Function to generate a PDF report from the summary data.

    Args:
        file_name (str): The name of the output PDF file.
        summary (dict): A dictionary containing the summary data to include in the PDF.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(0, 10, "Reporte de Ventas", ln=True, align="C")
    pdf.ln(10)  # Add a line break

    # Add content
    pdf.set_font("Arial", size=12)
    for section, data in summary.items():
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, section, ln=True)
        pdf.set_font("Arial", size=12)
        for key, value in data.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)
        pdf.ln(5)  # Add a line break between sections

    # Save the PDF
    pdf.output(file_name)

# Change current working directory to data
os.chdir(DATA_DIR)

summary = generate_summary()
generate_pdf("sales_report.pdf", summary)