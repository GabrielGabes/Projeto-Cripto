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

NOME_MOEDA = 'TRX'
STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

# ----------------------------------------
# 📊 PERÍODO DO CANDLE, SELECIONAR 1 📊

CANDLE_PERIOD = Client.KLINE_INTERVAL_1HOUR
CLANDES_RODADOS = calculadora_candles(CANDLE_PERIOD, 'semana')

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
candles_historico = baixar_candles(OPERATION_CODE, '12/03/2024', '20/03/2024', CANDLE_PERIOD)

# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=candles_historico,
    strategy_function=utBotAlerts,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    atr_multiplier=2,
    atr_period=1,
    verbose=False,
)
lista
lista.append('UT BOTS'); df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)

# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=candles_historico,
    strategy_function=getMovingAverageRSIVolumeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    verbose=False,
)
lista.append('MA RSI e VOLUME'); df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - MA ANTECIPATION - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=candles_historico,
    strategy_function=getMovingAverageAntecipationTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    volatility_factor=0.5,
    fast_window=7,
    slow_window=40,
    verbose=False,
)
lista.append('MA ANTECIPATION'); df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=candles_historico,
    strategy_function=getMovingAverageTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    fast_window=7,
    slow_window=40,
    verbose=False,
)
lista.append('MA SIMPLES FALLBACK'); df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=candles_historico,
    strategy_function=getRsiTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    low=30,
    high=70,
    verbose=False,
)
lista.append('RSI'); df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
# ------------------------------------------------------------------------

print(f"\n{STOCK_CODE} - VORTEX - {str(CANDLE_PERIOD)}")
lista = backtestRunner(
    stock_data=candles_historico,
    strategy_function=getVortexTradeStrategy,
    periods=CLANDES_RODADOS,
    initial_balance=INITIAL_BALANCE,
    verbose=False,
)
lista.append('VORTEX'); df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0)

# ------------------------------------------------------------------------
df['Moeda'] = NOME_MOEDA
df['CANDLE_PERIOD'] = CANDLE_PERIOD
df['CLANDES_RODADOS'] = CLANDES_RODADOS
df
print("\n\n")

