# BIBLIOTECAS EXTRAS
import sys
import getpass # Verificando qual usuario esta executando o codigo
if getpass.getuser() == 'gabri': 
    print('g')
    sys.path.append(r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src")
elif getpass.getuser() == 'michael':
    print('m')
    sys.path.append(r"C:\Users\michael\OneDrive\Documentos\GitHub\Projeto-Cripto\RoboTraderBinance_1_4b\src")

from tests.calculadora_candles import calculadora_candles
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from tests.baixar_candles import baixar_candles

from modules.BinanceTraderBot import BinanceTraderBot
from binance.client import Client
from tests.backtestRunner import backtestRunner
from strategies.ut_bot_alerts import *
from strategies.moving_average_antecipation import getMovingAverageAntecipationTradeStrategy
from strategies.moving_average import getMovingAverageTradeStrategy
from strategies.rsi_strategy import getRsiTradeStrategy
from strategies.vortex_strategy import getVortexTradeStrategy
from strategies.ma_rsi_volume_strategy import getMovingAverageRSIVolumeStrategy

# ------------------------------------------------------------------------
# 🔎 AJUSTES BACKTESTS 🔎

NOME_MOEDA = 'XRP'
STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

# ----------------------------------------
# 📊 PERÍODO DO CANDLE, SELECIONAR 1 📊

CANDLE_PERIOD = Client.KLINE_INTERVAL_1HOUR

# exemplo de aplicação do robo por 3 semnas, mas não mais aplicavel
# pois agora escolhemos periodos para ser rodados
# CLANDES_RODADOS = calculadora_candles(CANDLE_PERIOD, 'semana')*3 

# ------------------------------------------------------------------------
# DATA FRAME PARA CAPTURAR SAIDAS
df = pd.DataFrame(columns=[
    'Estrategia', 'Data_Inicio', 'Data_Fim', 'Saldo_Final', 'Lucro_%', 'Total_Trades',
    'Trades_Lucrativos', 'Valor_Lucro_Total', 'Trades_Preuízo', 'Valor_Preuízo_Total',
    'Lucro_Médio_Trade', 'Lucro_%_Médio', 'Prejuízo_Médio_Trade', 'Prejuízo_%_Médio'
    ])

# ------------------------------------------------------------------------
# ⏬ SELEÇÃO DE ESTRATÉGIAS ⏬

# devTrader = BinanceTraderBot(
#     stock_code=STOCK_CODE,
#     operation_code=OPERATION_CODE,
#     traded_quantity=0,
#     traded_percentage=100,
#     candle_period=CANDLE_PERIOD,
#     # volatility_factor=VOLATILITY_FACTOR,
# )
# devTrader.updateAllData()
# devTrader.stock_data

DEFAULT_START_DATE = '07/05/2025 12:00'
DEFAULT_END_DATE = '17/05/2025 02:00'
dados_candles = baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True)

# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=dados_candles,
    strategy_function=utBotAlerts,
    initial_balance=INITIAL_BALANCE,
    atr_multiplier=2,
    atr_period=1,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)

# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=dados_candles,
    strategy_function=getMovingAverageRSIVolumeStrategy,
    initial_balance=INITIAL_BALANCE,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - MA ANTECIPATION - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=dados_candles,
    strategy_function=getMovingAverageAntecipationTradeStrategy,
    initial_balance=INITIAL_BALANCE,
    volatility_factor=0.5,
    fast_window=7,
    slow_window=40,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=dados_candles,
    strategy_function=getMovingAverageTradeStrategy,
    initial_balance=INITIAL_BALANCE,
    fast_window=7,
    slow_window=40,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=dados_candles,
    strategy_function=getRsiTradeStrategy,
    initial_balance=INITIAL_BALANCE,
    low=30,
    high=70,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - VORTEX - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=dados_candles,
    strategy_function=getVortexTradeStrategy,
    initial_balance=INITIAL_BALANCE,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0)

# ------------------------------------------------------------------------
df['Moeda'] = NOME_MOEDA
df['CANDLE_PERIOD'] = CANDLE_PERIOD
df['Saldo_Inicial'] = INITIAL_BALANCE
# print(pd.concat([df.head(5), df.tail(5)], axis=0))
print(df)

print("\n\n")