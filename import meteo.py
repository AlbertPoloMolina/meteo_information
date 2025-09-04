import requests
import pandas as pd
from datetime import datetime, timedelta

url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-12-01T00%3A00%3A00UTC/fechafin/2024-01-01T23%3A59%3A00UTC/estacion/8500A'
headers = {
    'accept': 'application/json',
    'api_key': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcG9sb21vQHVvYy5lZHUiLCJqdGkiOiI2MDUyMDYxNC05MzIxLTRlYjgtOWZlYi0yZjQ5MjM0NzIwYTciLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcwMjU0OTQ0OCwidXNlcklkIjoiNjA1MjA2MTQtOTMyMS00ZWI4LTlmZWItMmY0OTIzNDcyMGE3Iiwicm9sZSI6IiJ9.dOAqVM7vBQaSUY_cVAcclBSyVj_NNpZSfpaTDjEsK4s'
}

# Obtener la fecha de ayer
fecha_ayer = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SUTC')
fecha_inicio = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SUTC')

# Modificar la URL para usar la fecha de ayer como fecha de fin
url = url.replace('2023-12-01T00%3A00%3A00UTC', f'{fecha_inicio}')
url = url.replace('2024-01-01T23%3A59%3A00UTC', f'{fecha_ayer}')

# Realizar la solicitud a la API
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtener los datos reales utilizando la URL proporcionada por la API
    datos_url = response.json().get('datos', '')

    
    response_datos = requests.get(datos_url)
    datos = response_datos.json()

    # Crear un DataFrame con los datos
    df_actuales = pd.DataFrame(datos)


# Ruta del archivo Excel existente
archivo_existente = r'C:\Users\albert\iCloudDrive\Documents\UOC\LlumPV\datos_meteorologicos.xlsx'

# Cargar el archivo Excel existente
try:
    df_existente = pd.read_excel(archivo_existente)
except FileNotFoundError:
    print("Archivo existente no encontrado. Se creará uno nuevo.")
    df_existente = pd.DataFrame()  # Crear un DataFrame vacío si el archivo no existe

# Combinar los datos actuales con los existentes
if not df_existente.empty:
    df_combinado = pd.concat([df_existente, df_actuales])
else:
    df_combinado = df_actuales

# Eliminar duplicados basándose en la columna "fecha"
df_combinado = df_combinado.drop_duplicates(subset="fecha")

# Guardar el archivo Excel actualizado
df_combinado.to_excel(archivo_existente, index=False)