import requests
import time
import datetime
from consulta_tendencias import consulta
from price_variation import build_variation_table

# Substitua pelos seus valores
TELEGRAM_BOT_TOKEN = "7446801344:AAHenxPWZzBffuowmaTWISyksUIsvBltkIg"
CHAT_ID = "-4628628345"

import random
import string

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Loop para executar todo primeiro minuto após a virada de hora (exemplo: 01:01, 02:01, etc.)
while True:
    now = datetime.datetime.now()
    if now.minute == 1 and now.second < 5:  # Executa entre 01:01:00 e 01:01:05 para segurança
        try:
            message = consulta()
            send_telegram_message(message)

            message2 = build_variation_table()
            send_telegram_message(message2)

            print(f"Mensagens enviadas ao Telegram às {now.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Erro ao executar consultas ou enviar mensagens: {e}")

        time.sleep(60)  # Espera 1 minuto para evitar execução dupla
    else:
        time.sleep(90)  # Checa a cada 5 segundos até chegar o momento certo
