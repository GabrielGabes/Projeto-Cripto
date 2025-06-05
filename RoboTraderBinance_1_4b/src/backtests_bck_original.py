# BIBLIOTECAS EXTRAS
import sys
sys.path.append(r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src")

from modules.BinanceTraderBot import BinanceTraderBot
from binance.client import Client
from tests.backtestRunner_bck_original import backtestRunner
from strategies.ut_bot_alerts import *
from strategies.moving_average_antecipation import getMovingAverageAntecipationTradeStrategy
from strategies.moving_average import getMovingAverageTradeStrategy
from strategies.rsi_strategy import getRsiTradeStrategy
from strategies.vortex_strategy import getVortexTradeStrategy
from strategies.ma_rsi_volume_strategy import getMovingAverageRSIVolumeStrategy

# ------------------------------------------------------------------------
# 🔎 AJUSTES BACKTESTS 🔎

STOCK_CODE = "XRP"  # Código da Criptomoeda
OPERATION_CODE = STOCK_CODE + "USDT"  # Código da operação (cripto + moeda)
INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

# ----------------------------------------
# 📊 PERÍODO DO CANDLE, SELECIONAR 1 📊

CANDLE_PERIOD = Client.KLINE_INTERVAL_1HOUR
# CANDLE_PERIOD = Client.KLINE_INTERVAL_15MINUTE
CLANDES_RODADOS = 7 * 24

# ------------------------------------------------------------------------
# ⏬ SELEÇÃO DE ESTRATÉGIAS ⏬

devTrader = BinanceTraderBot(
    stock_code=STOCK_CODE,
    operation_code=OPERATION_CODE,
    traded_quantity=0,
    traded_percentage=100,
    candle_period=CANDLE_PERIOD,
    # volatility_factor=VOLATILITY_FACTOR,
)
devTrader.updateAllData()
print(devTrader.stock_data.head(3))
print(devTrader.stock_data.tail(3))

# print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
# backtestRunner(
#     stock_data=devTrader.stock_data,
#     strategy_function=utBotAlerts,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     atr_multiplier=2,
#     atr_period=1,
#     verbose=False,
# )
# devTrader.updateAllData()

from tests.baixar_candles import baixar_candles
DEFAULT_START_DATE = '28/05/2025 10:00'
DEFAULT_END_DATE = '04/06/2025 10:00'
dados = baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True)

print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getMovingAverageRSIVolumeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    verbose=False,
)

# print(f"\n{STOCK_CODE} - MA ANTECIPATION - {str(CANDLE_PERIOD)}")
# backtestRunner(
#     stock_data=devTrader.stock_data,
#     strategy_function=getMovingAverageAntecipationTradeStrategy,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     volatility_factor=0.5,
#     fast_window=7,
#     slow_window=40,
#     verbose=False,
# )

# print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
# backtestRunner(
#     stock_data=devTrader.stock_data,
#     strategy_function=getMovingAverageTradeStrategy,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     fast_window=7,
#     slow_window=40,
#     verbose=False,
# )

# print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
# backtestRunner(
#     stock_data=devTrader.stock_data,
#     strategy_function=getRsiTradeStrategy,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     low=30,
#     high=70,
#     verbose=False,
# )

# print(f"\n{STOCK_CODE} - VORTEX - {str(CANDLE_PERIOD)}")
# backtestRunner(
#     stock_data=devTrader.stock_data,
#     strategy_function=getVortexTradeStrategy,
#     periods=CLANDES_RODADOS,
#     initial_balance=INITIAL_BALANCE,
#     verbose=False,
# )


# print("\n\n")
