# Instale a biblioteca se ainda não a tiver:
# pip install python-binance

from binance.client import Client
import pandas as pd

# Se necessário, insira suas credenciais (algumas funções podem ser acessadas sem chave, mas é recomendável utilizar a API key para evitar limitações)
api_key = 'SUA_API_KEY'
api_secret = 'SEU_API_SECRET'

client = Client(api_key, api_secret)

def carregando_dados_historicos(moeda, interval, start_str):
    # Obtenha os dados históricos de SOL/USDT
    klines = client.get_historical_klines(moeda, interval, start_str, end_str)

    # Converta os dados para um DataFrame do pandas e nomeie as colunas
    df = pd.DataFrame(klines, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume'
    ])

    # Converta os timestamps de milissegundos para datetime
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    # Converta as colunas de valores para numéricas
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col])

    return df

carregando_dados_historicos("SOLUSDT", Client.KLINE_INTERVAL_30MINUTE,
                            "2024-01-01", "2024-12-31")