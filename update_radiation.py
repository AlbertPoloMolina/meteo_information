import requests
import pandas as pd
from io import StringIO
import os
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry

# Configuración de la sesión con reintentos
session = requests.Session()
retries = Retry(
    total=5,  # número máximo de reintentos
    backoff_factor=2,  # espera exponencial entre intentos (2s, 4s, 8s...)
    status_forcelist=[500, 502, 503, 504],  # errores que se reintentan
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# URL de radiación
url = 'https://opendata.aemet.es/opendata/api/red/especial/radiacion'
headers = {
    'accept': 'application/json',
    'api_key': os.getenv("AEMET_API_KEY"),
    'User-Agent': 'meteo-bot/1.0 (github actions)'
}

df_valencia = pd.DataFrame()

try:
    response_rad = session.get(url, headers=headers, timeout=30)
    response_rad.raise_for_status()

    if response_rad.status_code == 200:
        response_json = response_rad.json()
        if 'datos' in response_json:
            datos_url_rad = response_json['datos']
            datos_texto = session.get(datos_url_rad, timeout=30).text

            # Saltar cabeceras y leer CSV
            data_to_text = '\n'.join(datos_texto.split('\n')[2:])
            df = pd.read_csv(StringIO(data_to_text), sep=';')

            # Filtrar estación de Valencia
            df_valencia = df[df['Estación'] == 'Valencia Aeropuerto'].copy()

            # Añadir la fecha desde la cabecera del archivo
            df_valencia.loc[:, 'Fecha'] = datos_texto.split('\r\n')[1]

except requests.exceptions.RequestException as e:
    print(f"Error al conectar con la API de AEMET: {e}")

# Guardar resultados si hay datos
if not df_valencia.empty:
    archivo_csv = 'datos_radiacion.csv'

    if os.path.exists(archivo_csv):
        df_existente = pd.read_csv(archivo_csv, encoding='utf-8', header=0)
        df_combinado = pd.concat([df_existente, df_valencia])
        df_combinado = df_combinado.drop_duplicates()
    else:
        df_combinado = df_valencia

    df_combinado.to_csv(archivo_csv, index=False, encoding='utf-8')
    print("Archivo de radiación actualizado correctamente.")
else:
    print("No se obtuvieron datos de radiación de la API.")


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





