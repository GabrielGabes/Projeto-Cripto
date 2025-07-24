# BIBLIOTECAS EXTRAS
import sys
import getpass # Verificando qual usuario esta executando o codigo
if getpass.getuser() == 'gabri': 
    print('g')
    sys.path.append(r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src")
elif getpass.getuser() == 'michael':
    print('m')
    sys.path.append(r"C:\Users\michael\OneDrive\Documentos\GitHub\Projeto-Cripto\RoboTraderBinance_1_4b\src")

from dotenv import load_dotenv

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from tests.baixar_candles import baixar_candles

from binance.client import Client
from tests.backtestRunner import backtestRunner

from datetime import datetime, timedelta

import pandas as pd
import pytz
import os

# Carrega credenciais do .env
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")
client = Client(api_key, secret_key)

NOME_MOEDA = 'BTC'
CANDLE_PERIOD = '15m'

# ------------------------------------------------------------------------
# 🔎 AJUSTES BACKTESTS 🔎

STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

# intervalos_tempo = ['01/12/2024 00:00', '02/12/2024 09:00']
# intervalos_tempo = ['22/12/2024 00:00', '31/12/2024 04:00']
intervalos_tempo = ['22/12/2024 00:00', '26/12/2024 04:00']

dados_candles = baixar_candles(OPERATION_CODE, intervalos_tempo[0], intervalos_tempo[1], CANDLE_PERIOD)
print(dados_candles.shape)

# ------------------------------------------------------------------------
# ⏬ SELEÇÃO DE ESTRATÉGIAS ⏬

from strategies.moving_average import *

final_result, price_decision_metrics = backtestRunner(
    stock_data=dados_candles,
<<<<<<< Updated upstream
    strategy_function=getMovingAverageTradeStrategy,
    nome_estrategia=getMovingAverageTradeStrategy,
=======
    strategy_function=getRsiTradeStrategy,
    nome_estrategia="teste",
>>>>>>> Stashed changes
    initial_balance=INITIAL_BALANCE,
    start_date=intervalos_tempo[0],
    end_date=intervalos_tempo[1],
    verbose=False)

print(price_decision_metrics.columns)
print(pd.concat([price_decision_metrics.head(), price_decision_metrics.tail()], axis=0))
print(price_decision_metrics['open_time_join'][118:130])
print(price_decision_metrics['acao_tomada'].value_counts())