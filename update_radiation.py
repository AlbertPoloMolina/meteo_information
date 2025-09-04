import requests
import pandas as pd
from io import StringIO
import os
from datetime import datetime

url = 'https://opendata.aemet.es/opendata/api/red/especial/radiacion'
headers = {
    'accept': 'application/json',
    'api_key': os.getenv("AEMET_API_KEY"),
    'User-Agent': 'meteo-bot/1.0 (github actions)'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.ResquestException as e:
    print(f"Error al conectar con la API de AEMET: {e}")
    
if response_rad.status_code == 200:
    response_json = response_rad.json()
    if 'datos' in response_json:
        datos_url_rad = response_json['datos']
        datos_texto = requests.get(datos_url_rad).text
        data_to_text = '\n'.join(datos_texto.split('\n')[2:])
        df = pd.read_csv(StringIO(data_to_text), sep=';')
        df_valencia = df[df['Estación'] == 'Valencia Aeropuerto'].copy()
        df_valencia.loc[:, 'Fecha'] = datos_texto.split('\r\n')[1]

        archivo_csv = 'datos_radiacion.csv'

        # Cargar CSV existente o crear uno nuevo
        if os.path.exists(archivo_csv):
            df_existente = pd.read_csv(archivo_csv)
            df_combinado = pd.concat([df_existente, df_valencia])
            df_combinado = df_combinado.drop_duplicates()
        else:
            df_combinado = df_valencia


        df_combinado.to_csv(archivo_csv, index=False, encoding='utf-8')

# Enviar notificación a Telegram
API_KEY_TELEGRAM = os.getenv("API_KEY_TELEGRAM")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
mensaje = f"Radiación actualizada correctamente: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

url_telegram = f"https://api.telegram.org/bot{API_KEY_TELEGRAM}/sendMessage"
payload = {
    'chat_id': TELEGRAM_CHAT_ID,
    'text': mensaje
}
try:
    requests.post(url_telegram, data=payload)
except Exception as e:
    print(f"Error enviando mensaje a Telegram: {e}")






