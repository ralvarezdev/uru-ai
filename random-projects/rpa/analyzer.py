import os

from fpdf import FPDF
import pandas as pd

from constants import (
    SALES_XLSX,
    DATA_DIR,
    FIRA_CODE_REGULAR,
    FIRA_CODE_BOLD,
    FONTS_DIR
)

# Load the Excel file
data = pd.read_excel(SALES_XLSX, engine="openpyxl")

# Rename the columns for better readability
columns_renamed = {
    'Costo Vehículo': 'Costo de Vehículo',
    'Precio Venta sin IGV': 'Precio Venta de Vehículo sin IGV',
    'Precio Venta Real': 'Precio Venta de Vehículo con IGV',
    'Ganancia': 'Ganancia por Venta',
}
data.rename(columns=columns_renamed, inplace=True)

# Generate a profit column
data['Ganancia por Venta'] = data['Precio Venta de Vehículo sin IGV'] - data[(
    'Costo de Vehículo')]

# Define the numerical columns to analyze and their statistics functions
numerical_columns = [
    'Costo de Vehículo',
    'Precio Venta de Vehículo sin IGV',
    'Precio Venta de Vehículo con IGV',
    'Ganancia por Venta',
]
stats_fns = ['min', 'max', 'mean', 'median', 'std']
stats_fns_renamed = {
    'min': 'Mínimo',
    'max': 'Máximo',
    'mean': 'Media',
    'median': 'Mediana',
    'std': 'Desviación Estándar'
}
numerical_data = data[numerical_columns]

# Get the min, max, mean, median, and standard deviation for the numerical columns
numerical_stats = numerical_data.agg(stats_fns)
numerical_stats.rename(index=stats_fns_renamed, inplace=True)

# Define the numerical columns to analyze plus the 'Fecha' column
numerical_with_dt_columns = ['Fecha',*numerical_columns]
numerical_with_dt_data = data[numerical_with_dt_columns]

# Generate an anual numerical summary
anual_summary = numerical_with_dt_data.groupby(data['Fecha'].dt.year).agg({
    'Costo de Vehículo': stats_fns,
    'Precio Venta de Vehículo sin IGV': stats_fns,
    'Precio Venta de Vehículo con IGV': stats_fns,
    'Ganancia por Venta': stats_fns
})
anual_summary.columns = [
    f"{col} Anual ({stats_fns_renamed[stat]})" for col, stat in anual_summary.columns
]
#anual_summary.rename(
#    index=stats_fns_renamed,
#    columns = [f"{col} Anual ({stat})" for col, stat in anual_summary.columns]
#)

# Generate a quarterly numerical summary
quarterly_summary = numerical_with_dt_data.groupby(data['Fecha'].dt.to_period('Q')).agg({
    'Costo de Vehículo': stats_fns,
    'Precio Venta de Vehículo sin IGV': stats_fns,
    'Precio Venta de Vehículo con IGV': stats_fns,
    'Ganancia por Venta': stats_fns
})
quarterly_summary.columns = [
    f"{col} Trimestral ({stats_fns_renamed[stat]})" for col, stat in quarterly_summary.columns
]
#anual_summary.rename(
#    index=stats_fns_renamed,
#    columns = [f"{col} Trimestral ({stat})" for col, stat in
#               quarterly_summary.columns]
#)

# Remove hour from 'Fecha' column
data['Fecha'] = data['Fecha'].dt.date

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
    return {
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
        "Estadísticas numéricas": numerical_stats.to_dict(),
        "Resumen anual": anual_summary.to_dict(),
        "Resumen trimestral": quarterly_summary.to_dict(),
    }

def generate_pdf(
    file_name: str,
    summary: dict,
    fonts_dir=FONTS_DIR,
    output_dir=DATA_DIR
):
    """
    Function to generate a PDF report from the summary data.

    Args:
        file_name (str): The name of the output PDF file.
        summary (dict): A dictionary containing the summary data to include in the PDF.
        fonts_dir (str): The directory where the font files are located.
        output_dir (str): The directory where the PDF file will be saved.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add the Fira Code font
    if fonts_dir:
        os.chdir(fonts_dir)
    pdf.add_font('Fira Code', '', FIRA_CODE_REGULAR, uni=True)
    pdf.add_font('Fira Code', 'B', FIRA_CODE_BOLD, uni=True)

    # Set the font to Fira Code
    pdf.set_font("Fira Code", size=12)

    # Add a title
    pdf.set_font("Fira Code", style="B", size=16)
    pdf.cell(0, 10, "Reporte de Ventas", ln=True, align="C")
    pdf.ln(10)  # Add a line break

    # Add content
    pdf.set_font("Fira Code", size=12)
    for section, data in summary.items():
        pdf.set_font("Fira Code", style="B", size=12)
        pdf.cell(0, 10, section, ln=True)
        pdf.set_font("Fira Code", size=12)
        for key, value in data.items():
            pdf.cell(0, 5, f"{key}: {value}", ln=True)
        pdf.ln(5)  # Add a line break between sections

    # Save the PDF
    if output_dir:
        os.chdir(output_dir)
    pdf.output(file_name)

# Change current working directory to data
os.chdir(DATA_DIR)

summary = generate_summary()
generate_pdf("sales_report.pdf", summary)