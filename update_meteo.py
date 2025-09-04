import requests
import pandas as pd
from datetime import datetime, timedelta
import os

url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-12-01T00%3A00%3A00UTC/fechafin/2024-01-01T23%3A59%3A00UTC/estacion/8500A'
headers = {
    'accept': 'application/json',
    'api_key': os.getenv("AEMET_API_KEY")
    'User-Agent': 'meteo-bot/1.0 (github actions)'
}

# Obtener la fecha de ayer
fecha_ayer = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SUTC')
fecha_inicio = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SUTC')

# Modificar la URL para usar la fecha de ayer como fecha de fin
url = url.replace('2023-12-01T00%3A00%3A00UTC', f'{fecha_inicio}')
url = url.replace('2024-01-01T23%3A59%3A00UTC', f'{fecha_ayer}')

# Realizar la solicitud a la API
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.ResquestException as e:
    print(f"Error al conectar con la API de AEMET: {e}")

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Obtener los datos reales utilizando la URL proporcionada por la API
    datos_url = response.json().get('datos', '')

    response_datos = requests.get(datos_url)
    datos = response_datos.json()

    # Crear un DataFrame con los datos
    df_actuales = pd.DataFrame(datos)

# Ruta del archivo CSV existente
archivo_existente = 'datos_meteorologicos.csv'

# Cargar el archivo CSV existente
try:
    df_existente = pd.read_csv(archivo_existente)
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

# Guardar el archivo CSV actualizado
df_combinado.to_csv(archivo_existente, index=False, encoding='utf-8')

# Enviar notificación a Telegram
API_KEY_TELEGRAM = os.getenv("API_KEY_TELEGRAM")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
mensaje = f"Meteo actualizado correctamente: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

url_telegram = f"https://api.telegram.org/bot{API_KEY_TELEGRAM}/sendMessage"
payload = {
    'chat_id': TELEGRAM_CHAT_ID,
    'text': mensaje
}
try:
    requests.post(url_telegram, data=payload)
except Exception as e:
    print(f"Error enviando mensaje a Telegram: {e}")






