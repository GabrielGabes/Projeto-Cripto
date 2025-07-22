from binance.client import Client
from dotenv import load_dotenv
import requests

import pandas as pd
import numpy as np
import datetime
import threading
import os
import time
import traceback
import io

#================================================================================# Configurações do bot de status
BOT_TOKEN_STATUS = '8013077654:AAFWFkaRcWDCRHcCSXbjn877CNs9wQ4hmBA'
CHAT_ID_STATUS = '-1002871039327'

def send_status_message(mensagem):
    print('Bot online ✅')
    url = f"https://api.telegram.org/bot{BOT_TOKEN_STATUS}/sendMessage"
    payload = {
        'chat_id': CHAT_ID_STATUS,
        'text': mensagem,
        'parse_mode': 'Markdown' 
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem: {response.text}")
    except Exception as e:
        print(f"Exceção ao enviar mensagem: {e}")

def obter_intervalo_do_info():
    url = f"https://api.telegram.org/bot{BOT_TOKEN_STATUS}/getChat"
    params = {'chat_id': CHAT_ID_STATUS}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            descricao = data.get('result', {}).get('description', '')
            intervalo = float(descricao.strip()) * 60  # minutos para segundos
            intervalo = max(1, int(intervalo))  # garante pelo menos 1 segundo
            print(f"Intervalo lido da descrição: {intervalo} seg")
            return intervalo
        else:
            print(f"Erro ao obter descrição: {response.text}")
    except Exception as e:
        print(f"Erro ao ler info: {e}")
    return 600  # valor padrão em segundos (10 minutos)

def verificar_status_robo():
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem = f"RPA NOVAS MOEDAS: Online {agora} ✅"
    send_status_message(mensagem)

    intervalo = obter_intervalo_do_info()
    threading.Timer(intervalo, verificar_status_robo).start()
    
#================================================================================
# Substitua pelos seus valores
TELEGRAM_BOT_TOKEN = "7446801344:AAHenxPWZzBffuowmaTWISyksUIsvBltkIg"
CHAT_ID = "-4628628345"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
            "chat_id": CHAT_ID, 
            "text": message,
            "parse_mode": "HTML"
            # disable_web_page_preview=True  # opcional: oculta o preview do link
            }
    requests.post(url, data=data)

def formatar_mensagem_telegram(lista):
    texto = ''
    for moeda in lista:
        texto = texto + '\n' + moeda
    return texto
#================================================================================
# Carregar chaves da API da Binance (opcional, só é necessário para chamadas privadas)
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

# caminho_diretorio = os.path.dirname(os.path.abspath(__file__))
caminho_diretorio = os.getcwd()
caminho_arquivo = os.path.join(caminho_diretorio, 'dados_historicos.parquet')
df = pd.read_parquet(caminho_arquivo)

# VERIFICANDO SE HÁ ALGUMA MOEDA NOVA:
# Inicializar cliente
client = Client(API_KEY, API_SECRET)

verificar_status_robo()

while True:
    # Obter todos os pares de negociação da Binance
    try: 
        tickers = client.get_exchange_info()['symbols']
        print(str(pd.Timestamp.now()), ': Execução')
    except requests.exceptions.ReadTimeout:
        print(str(pd.Timestamp.now()), ": Timeout na API da Binance. Tentando novamente...")
        time.sleep(30)

    try:
        # Gerar conjunto de todos os símbolos disponíveis
        moedas_novas = []
        for item in tickers:

            if 'USDT' == item['symbol'][-4:]:

                if item['symbol'][:-4] not in df['moeda'].values:
                    nome_moeda = item['symbol'][:-4]
                    print(str(pd.Timestamp.now()), ":nova moeda encontrada ->", nome_moeda)
                    moedas_novas.append(nome_moeda)

        # Opcional: salvar novas moedas no histórico
        if moedas_novas:
            mensagem = formatar_mensagem_telegram(moedas_novas)
            send_telegram_message(mensagem)

            df_novas = pd.DataFrame({'moeda': moedas_novas, 'data': pd.Timestamp.now()})
            df = pd.concat([df, df_novas])
            df.to_parquet(caminho_arquivo, index=False)
        moedas_novas = []
    except:
        f = io.StringIO()
        traceback.print_exc(file=f)
        mensagem = '⚠️ Erro fatal! Código encerrado:\n' + f.getvalue()
        print(str(pd.Timestamp.now()), ':')
        send_telegram_message(mensagem)
        break

    time.sleep(60*2)