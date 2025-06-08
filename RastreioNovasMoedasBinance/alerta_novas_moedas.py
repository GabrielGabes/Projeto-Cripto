from binance.client import Client
import os
from dotenv import load_dotenv

import pandas as pd
import numpy as np

import time
import traceback
import io

# Substitua pelos seus valores
TELEGRAM_BOT_TOKEN = "7446801344:AAHenxPWZzBffuowmaTWISyksUIsvBltkIg"
CHAT_ID = "-4628628345"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
            "chat_id": CHAT_ID, 
            "text": message,
            "parse_mode": "HTML",
            # disable_web_page_preview=True  # opcional: oculta o preview do link
            }
    requests.post(url, data=data)

def formatar_mensagem_telegram(lista):
    texto = ''
    for moeda in lista:
        texto = texto + '\n' + moeda
    return texto

# Carregar chaves da API da Binance (opcional, só é necessário para chamadas privadas)
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

df = pd.read_parquet('dados_historicos')

# VERIFICANDO SE HÁ ALGUMA MOEDA NOVA:

# Inicializar cliente
client = Client(API_KEY, API_SECRET)

while True:
    try:
        # Obter todos os pares de negociação da Binance
        tickers = client.get_exchange_info()['symbols']

        # Gerar conjunto de todos os símbolos disponíveis
        moedas_novas = []
        for item in tickers:

            if 'USDT' == item['symbol'][-4:]:

                if item['symbol'][:-4] not in df['moeda'].values:
                    nome_moeda = item['symbol'][:-4]
                    print('nova moeda encontrada:', nome_moeda)
                    moedas_novas.append(nome_moeda)

        # Opcional: salvar novas moedas no histórico
        if moedas_novas:
            mensagem = formatar_mensagem_telegram(moedas_novas)
            send_telegram_message(mensagem)

            df_novas = pd.DataFrame({'moeda': moedas_novas, 'data': pd.Timestamp.now()})
            df = pd.concat([df, df_novas], ignore_index=True)
            df.to_parquet('dados_historicos.parquet', index=False)
        moedas_novas = []
    except:
        f = io.StringIO()
        traceback.print_exc(file=f)
        mensagem = '⚠️ Erro fatal! Código encerrado:\n' + f.getvalue()
        send_telegram_message(mensagem)
        break
    print('execução:', pd.Timestamp.now())
    time.sleep(60*2)