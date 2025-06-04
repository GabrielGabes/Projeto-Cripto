# BIBLIOTECAS EXTRAS
import sys
sys.path.append(r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src")
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
CLANDES_RODADOS = calculadora_candles(CANDLE_PERIOD, 'dia')

# ------------------------------------------------------------------------
# DATA FRAME PARA CAPTURAR SAIDAS
df = pd.DataFrame(columns=[
                            'Balanço final', # 'balance'
                            'Lucro/prejuízo percentual', # 'profit_percentage'
                            'Total de operações', # 'trades'
                            'ESTRATÉGIA'
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

# DEFAULT_START_DATE = '10/06/2024 23:00'
# DEFAULT_END_DATE = '17/06/2025 23:00'
DEFAULT_START_DATE = '28/05/2025 03:00'
DEFAULT_END_DATE = '04/06/2025 02:00'
dados = baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True)

print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")

print('Código 1', '*'*120)
# teste codigo 1
from tests.backtestRunner import backtestRunner
backtestRunner(
    stock_data=dados,
    strategy_function=getMovingAverageRSIVolumeStrategy,
    initial_balance=INITIAL_BALANCE,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    verbose=False,
)
# print(dados.head(3))
# print(dados.tail(3))

# print('Código 2', '*'*120)
# # teste codigo 2
# from tests.backtestRunner_bck_original_ajustado import backtestRunner
# lista = backtestRunner(
#     stock_data=baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True),
#     strategy_function=getMovingAverageRSIVolumeStrategy,
#     initial_balance=INITIAL_BALANCE,
#     start_date=DEFAULT_START_DATE,
#     end_date=DEFAULT_END_DATE,
#     verbose=False,
# )

# print('Código 3', '*'*120)
# # teste codigo 3
# from tests.backtestRunner_bck_original import backtestRunner
# lista = backtestRunner(
#     stock_data=baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=False),
#     strategy_function=getMovingAverageRSIVolumeStrategy,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     verbose=False,
# )

# print('Código 4', '*'*120)
# # teste codigo 4
# CANDLE_PERIOD = 30
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
# from tests.backtestRunner_bck_original import backtestRunner
# backtestRunner(
#     stock_data=devTrader.stock_data,
#     strategy_function=getMovingAverageRSIVolumeStrategy,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     verbose=False,
# )