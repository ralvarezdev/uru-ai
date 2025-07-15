import pandas as pd

from constants import (
    SALES_XLSX
)

def analyze_sales_data(sales_xlsx: str = SALES_XLSX):
    """
    Function to analyze sales data from an Excel file and generate a summary report.
    """
    # Load the Excel file
    data = pd.read_excel(sales_xlsx, engine="openpyxl")

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

    # Generate the profits per segment
    segment_profit = data.groupby('Segmento')['Ganancia por Venta'].sum().sort_values(ascending=False)

    # Generate the profits per channel
    channel_profit = data.groupby('Canal')['Ganancia por Venta'].sum().sort_values(ascending=False)

    # Generate the profits per location
    location_profit = data.groupby('Sede')['Ganancia por Venta'].sum().sort_values(ascending=False)

    return [
        segment_counts,
        top_counts,
        segment_profit,
        channel_profit,
        location_profit,
        numerical_stats,
        anual_summary,
        quarterly_summary
    ]