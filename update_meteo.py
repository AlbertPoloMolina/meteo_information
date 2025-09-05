import requests
import pandas as pd
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter, Retry
import os

# Configuración de reintentos
session = requests.Session()
retries = Retry(
    total=5,  # número máximo de intentos
    backoff_factor=2,  # espera exponencial: 2s, 4s, 8s...
    status_forcelist=[500, 502, 503, 504],  # errores de servidor que se reintentan
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Construcción de la URL dinámica
url_base = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2023-12-01T00%3A00%3A00UTC/fechafin/2024-01-01T23%3A59%3A00UTC/estacion/8500A'
headers = {
    'accept': 'application/json',
    'api_key': os.getenv("AEMET_API_KEY"),
    'User-Agent': 'meteo-bot/1.0 (github actions)'
}

# Fechas dinámicas (últimos 30 días hasta ayer)
fecha_ayer = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SUTC')
fecha_inicio = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SUTC')

url = url_base.replace('2023-12-01T00%3A00%3A00UTC', fecha_inicio)
url = url.replace('2024-01-01T23%3A59%3A00UTC', fecha_ayer)

df_actuales = pd.DataFrame()

try:
    # Primer request a la API
    response = session.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    if response.status_code == 200:
        # Obtener URL real de los datos
        datos_url = response.json().get('datos', '')
        if datos_url:
            response_datos = session.get(datos_url, timeout=30)
            response_datos.raise_for_status()
            datos = response_datos.json()

            # Crear DataFrame con los datos obtenidos
            df_actuales = pd.DataFrame(datos)

except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API de AEMET: {e}")

# Procesar el CSV existente y combinar datos
archivo_existente = 'datos_meteorologicos.csv'

if os.path.exists(archivo_existente):
    df_existente = pd.read_csv(archivo_existente, encoding='utf-8', header=0)
else:
    df_existente = pd.DataFrame()

if not df_actuales.empty:
    if not df_existente.empty:
        df_combinado = pd.concat([df_existente, df_actuales])
    else:
        df_combinado = df_actuales

    # Eliminar duplicados por fecha
    if "fecha" in df_combinado.columns:
        df_combinado = df_combinado.drop_duplicates(subset="fecha")

    # Guardar CSV actualizado
    df_combinado.to_csv(archivo_existente, index=False, encoding='utf-8')
    print("Archivo CSV actualizado correctamente.")
else:
    print("No se obtuvieron datos nuevos de la API.")



filas_antes = len(df_existente) if not df_existente.empty else 0
filas_despues = len(df_combinado)
filas_nuevas = filas_despues - filas_antes

# Enviar notificación a Telegram
API_KEY_TELEGRAM = os.getenv("API_KEY_TELEGRAM")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

mensaje = f"✅ Actualización completada.\nFilas antes: {filas_antes}\nFilas después: {filas_despues}\n➕ Nuevas filas: {filas_nuevas}"

url_telegram = f"https://api.telegram.org/bot{API_KEY_TELEGRAM}/sendMessage"
payload = {
    'chat_id': TELEGRAM_CHAT_ID,
    'text': mensaje
}
try:
    requests.post(url_telegram, data=payload)
except Exception as e:
    print(f"Error enviando mensaje a Telegram: {e}")


