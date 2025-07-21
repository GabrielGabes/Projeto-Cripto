# BIBLIOTECAS EXTRAS
import sys
sys.path.append(r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src")
from tests.calculadora_candles import calculadora_candles
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from tests.baixar_candles import baixar_candles
import warnings

from modules.BinanceTraderBot import BinanceTraderBot
from binance.client import Client
from tests.backtestRunner import backtestRunner

from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

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

intervalos_tempo = ['01/12/2024 00:00', '02/12/2024 09:00']

dados_candles = baixar_candles(OPERATION_CODE, intervalos_tempo[0], intervalos_tempo[1], CANDLE_PERIOD)
dados_candles.head()

# ------------------------------------------------------------------------
# DATA FRAME PARA CAPTURAR SAIDAS
df = pd.DataFrame(columns=[
'Estrategia', 'Data_Inicio', 'Data_Fim', 'Saldo_Final', 'Lucro_%', 'Total_Trades',
'Trades_Lucrativos', 'Valor_Lucro_Total', 'Trades_Preuízo', 'Valor_Preuízo_Total',
'Lucro_Médio_Trade', 'Lucro_%_Médio', 'Prejuízo_Médio_Trade', 'Prejuízo_%_Médio'
])

# ------------------------------------------------------------------------
# ⏬ SELEÇÃO DE ESTRATÉGIAS ⏬

from strategies.ut_bot_alerts import *

final_result, price_decision_metrics = backtestRunner(
    stock_data=dados_candles,
    strategy_function=utBotAlerts,
    nome_estrategia="utBotAlerts",
    initial_balance=INITIAL_BALANCE,
    start_date=intervalos_tempo[0],
    end_date=intervalos_tempo[1],
    verbose=False)

print(final_result)
print(price_decision_metrics)
print(price_decision_metrics.columns)
print(price_decision_metrics['open_time_join'][100:150])

print(price_decision_metrics['acao_tomada'].value_counts())


print(price_decision_metrics[pd.notnull(price_decision_metrics['acao_tomada'])])
print(price_decision_metrics[pd.notnull(price_decision_metrics['open_time_join'])])
