import os

import pandas as pd

from pdf import PDF
from constants import (
    DATA_DIR,
    FIRA_CODE_REGULAR,
    FIRA_CODE_BOLD,
    FONTS_DIR,
)

def generate_summary(
    segment_counts: pd.Series,
    top_counts: pd.DataFrame,
    numerical_stats: pd.DataFrame,
    anual_summary: pd.DataFrame,
    quarterly_summary: pd.DataFrame,
    segment_profit: pd.DataFrame,
    channel_profit: pd.DataFrame,
    location_profit: pd.DataFrame,
):
    """
    Function to generate a summary of the sales data.

    Args:
        segment_counts (pd.Series): Counts of sales by segment.
        top_counts (pd.DataFrame): DataFrame containing top counts for various categories.
        numerical_stats (pd.DataFrame): DataFrame with numerical statistics.
        anual_summary (pd.DataFrame): DataFrame with annual summary statistics.
        quarterly_summary (pd.DataFrame): DataFrame with quarterly summary statistics.
        segment_profit (pd.DataFrame): DataFrame with profits by segment.
        channel_profit (pd.DataFrame): DataFrame with profits by channel.
        location_profit (pd.DataFrame): DataFrame with profits by location.
    """
    return [
        {
            "Ventas por segmento": segment_counts.to_dict(),
            "Top 5 Canales con mayor cantidad de ventas": top_counts[
                'Canal'].to_dict(),
            "Top 5 Clientes con más compras": top_counts['Cliente'].to_dict(),
            "Top 5 Fechas donde se realizaron más ventas": top_counts[
                'Fecha'].to_dict(),
            "Top 5 Sedes con mayor cantidad de ventas": top_counts[
                'Sede'].to_dict(),
            "Top 5 Vendedores con más ventas realizadas": top_counts[
                'Vendedor'].to_dict(),
        },
        {
            "Ganancias por Segmento": segment_profit,
            "Ganancias por Canal": channel_profit,
            "Ganancias por Sede": location_profit,
        },
        {
            "Estadísticas numéricas": numerical_stats.to_dict(),
        },
        {
            "Resumen anual": anual_summary.to_dict(),
        },
        {
            "Resumen trimestral": quarterly_summary.to_dict(),
        }
    ]

def generate_pdf(
    file_name: str,
    summary: list,
    fonts_dir=FONTS_DIR,
    output_dir=DATA_DIR
):
    """
    Function to generate a PDF report from the summary data.

    Args:
        file_name (str): The name of the output PDF file.
        summary (list): A dictionary containing the summary data to include in the PDF.
        fonts_dir (str): The directory where the font files are located.
        output_dir (str): The directory where the PDF file will be saved.
    """
    pdf = PDF()
    pdf.add_page()

    # Add the Fira Code font
    if fonts_dir:
        os.chdir(fonts_dir)
    pdf.add_font('Fira Code', '', FIRA_CODE_REGULAR, uni=True, set_as_main=True)
    pdf.add_font('Fira Code', 'B', FIRA_CODE_BOLD, uni=True, set_as_main=True)

    # Add a title
    pdf.h1("Reporte de Ventas", align="C")

    # Add content
    for idx, page in enumerate(summary):
        for section, data in page.items():
            pdf.h2(section)
            for key, value in data.items():
                if isinstance(value, dict):
                    pdf.h3(key)
                    for sub_key, sub_value in value.items():
                        pdf.text(f"{sub_key}: {sub_value}", tabs=2,
                                 newline=False)
                    pdf.newline()
                else:
                    pdf.text(f"{key}: {value}", tabs=1, newline=False)
            pdf.newline()

        if idx < len(summary) - 1:
            pdf.add_page()

    # Save the PDF
    if output_dir:
        os.chdir(output_dir)
    pdf.output(file_name)