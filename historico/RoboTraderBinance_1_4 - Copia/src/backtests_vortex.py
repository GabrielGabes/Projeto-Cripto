from tests.calculadora_candles import calculadora_candles

from modules.BinanceTraderBot import BinanceTraderBot
from binance.client import Client
from tests.backtestRunner import backtestRunner
from strategies.ut_bot_alerts import *
from strategies.moving_average_antecipation import getMovingAverageAntecipationTradeStrategy
from strategies.moving_average import getMovingAverageTradeStrategy
from strategies.rsi_strategy import getRsiTradeStrategy
from strategies.vortex_strategy import getVortexTradeStrategy
from strategies.ma_rsi_volume_strategy import getMovingAverageRSIVolumeStrategy
from strategies.ton_strategy import getAdvancedTradeStrategy
# from strategies.ton_ma_rsi_volume_strategy import getCombinedTradeStrategyDistinctBuy

# ------------------------------------------------------------------------
# 🔎 AJUSTES BACKTESTS 🔎

STOCK_CODE = "ADA"  # Código da Criptomoeda
OPERATION_CODE = STOCK_CODE + "USDT" # Código da operação (cripto + moeda)
INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

# ----------------------------------------
# 📊 PERÍODO DO CANDLE, SELECIONAR 1 📊

CANDLE_PERIOD = Client.KLINE_INTERVAL_30MINUTE
CLANDES_RODADOS = calculadora_candles(CANDLE_PERIOD, 'semana')

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

print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=utBotAlerts,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    atr_multiplier=2,
    atr_period=1,
    verbose=False,
)

devTrader.updateAllData()

print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getMovingAverageRSIVolumeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    verbose=False,
)


print(f"\n{STOCK_CODE} - MA ANTECIPATION - {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getMovingAverageAntecipationTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    volatility_factor=0.5,
    fast_window=7,
    slow_window=40,
    verbose=False,
)

print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getMovingAverageTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    fast_window=7,
    slow_window=40,
    verbose=False,
)

print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getRsiTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    low=30,
    high=70,
    verbose=False,
)

print(f"\n{STOCK_CODE} - VORTEX - Candle de {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getVortexTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    verbose=False,
)

print(f"\n{STOCK_CODE} - Indicadores Avançados (Vortex + Outros) - Candle de {str(CANDLE_PERIOD)}")
backtestRunner(
    stock_data=devTrader.stock_data,
    strategy_function=getAdvancedTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    verbose=False,   
)


print("\n\n")
print("\n\n")
