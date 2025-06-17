from binance.client import Client
from dotenv import load_dotenv

import pandas as pd
import numpy as np

import os
import time
import traceback

# Carregar chaves da API da Binance (opcional, só é necessário para chamadas privadas)
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

# Inicializar cliente
client = Client(API_KEY, API_SECRET)

# Obter todos os pares de negociação da Binance
tickers = client.get_exchange_info()['symbols']

# Gerar conjunto de todos os símbolos disponíveis
symbol_set = []
for item in tickers:
    if 'USDT' == item['symbol'][-4:]:
    # if 'USDT' in item['symbol'][-4:]:
        symbol_set.append(item['symbol'].replace('USDT',''))
print(symbol_set)

df = pd.DataFrame(symbol_set, columns=['moeda'])
df['data_atual'] = pd.Timestamp.now()


caminho_diretorio = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(caminho_diretorio, 'dados_historicos.parquet')
df.to_parquet(caminho_arquivo, index=False)