# BIBLIOTECAS EXTRAS
import sys
sys.path.append("C:/Users/gabri/OneDrive/Documentos/PROJETOS PARADOS OU TERMINADOS/RoboTraderBinance_1_4/src")
from tests.calculadora_candles import calculadora_candles
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from modules.BinanceTraderBot import BinanceTraderBot
from binance.client import Client
from tests.backtestRunner_list import backtestRunner
from strategies.ut_bot_alerts import *
from strategies.moving_average_antecipation import getMovingAverageAntecipationTradeStrategy
from strategies.moving_average import getMovingAverageTradeStrategy
from strategies.rsi_strategy import getRsiTradeStrategy
from strategies.vortex_strategy import getVortexTradeStrategy
from strategies.ma_rsi_volume_strategy import getMovingAverageRSIVolumeStrategy

# ------------------------------------------------------------------------
# NOME_MOEDA = 'SOL'
# CANDLE_PERIOD = Client.KLINE_INTERVAL_1HOUR
# saida = 'semana'

def backtests_simulador(NOME_MOEDA, CANDLE_PERIOD, saida):
    # 🔎 AJUSTES BACKTESTS 🔎

    STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
    OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
    INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

    # ----------------------------------------
    # 📊 PERÍODO DO CANDLE, SELECIONAR 1 📊

    CLANDES_RODADOS = calculadora_candles(CANDLE_PERIOD, saida)
    # ------------------------------------------------------------------------
    # DATA FRAME PARA CAPTURAR SAIDAS
    df = pd.DataFrame(columns=[
                                'Balanço final', # 'balance'
                                'Lucro/prejuízo percentual', # 'profit_percentage'
                                'Total de operações', # 'trades'
                                'ESTRATÉGIA'
                            ])
    df

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

    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=utBotAlerts,
        nome_estrategia = "UT BOTS",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        atr_multiplier=2,
        atr_period=1,
        verbose=False,
    )
    lista
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    devTrader.updateAllData()
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageRSIVolumeStrategy,
        nome_estrategia = "MA RSI e VOLUME",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)

    # #######################################################################################################
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 7_40- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 7_40",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=7,
        slow_window=40,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 5_10- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 5_10",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=5,
        slow_window=10,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 5_13- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 5_13",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=5,
        slow_window=13,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 7_14- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 7_14",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=7,
        slow_window=14,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 8_16- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 8_16",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=8,
        slow_window=16,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 10_20- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 10_20",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=10,
        slow_window=20,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 9_21 - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 9_21",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=9,
        slow_window=21,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 10_50 - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 10_50",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=10,
        slow_window=50,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA ANTECIPATION 13_26 - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageAntecipationTradeStrategy,
        nome_estrategia = "MA ANTECIPATION 13_26",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        volatility_factor=0.5,
        fast_window=13,
        slow_window=26,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)

    # #######################################################################################################
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=7,
        slow_window=40,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 7_40- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 7_40",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=7,
        slow_window=40,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 5_10- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 5_10",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=5,
        slow_window=10,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 5_13- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 5_13",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=5,
        slow_window=13,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 7_14- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 7_14",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=7,
        slow_window=14,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 8_16- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 8_16",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=8,
        slow_window=16,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 10_20- {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 10_20",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=10,
        slow_window=20,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 9_21 - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 9_21",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=9,
        slow_window=21,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 10_50 - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 10_50",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=10,
        slow_window=50,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 13_26 - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getMovingAverageTradeStrategy,
        nome_estrategia = "MA SIMPLES FALLBACK 13_26",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        fast_window=13,
        slow_window=26,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # #######################################################################################################
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getRsiTradeStrategy,
        nome_estrategia = "RSI",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        low=30,
        high=70,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - VORTEX - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=devTrader.stock_data,
        strategy_function=getVortexTradeStrategy,
        nome_estrategia = "VORTEX",
        periods=CLANDES_RODADOS,
        initial_balance=INITIAL_BALANCE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print("\n\n")

    # ------------------------------------------------------------------------
    df['Moeda'] = NOME_MOEDA
    df['CANDLE_PERIOD'] = CANDLE_PERIOD
    df['CLANDES_RODADOS'] = CLANDES_RODADOS
    return df