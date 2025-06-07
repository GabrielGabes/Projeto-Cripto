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

def backtests_simulador(
        NOME_MOEDA, 
        CANDLE_PERIOD = '1h', 
        DEFAULT_START_DATE='12/03/2025 03:00',
        DEFAULT_END_DATE='15/03/2025 03:00'
        ):
    # ------------------------------------------------------------------------
    # 🔎 AJUSTES BACKTESTS 🔎

    STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
    OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
    INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL

    dados_candles = baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True)

    # ------------------------------------------------------------------------
    # DATA FRAME PARA CAPTURAR SAIDAS
    df = pd.DataFrame(columns=[
        'Estrategia', 'Data_Inicio', 'Data_Fim', 'Saldo_Final', 'Lucro_%', 'Total_Trades',
        'Trades_Lucrativos', 'Valor_Lucro_Total', 'Trades_Preuízo', 'Valor_Preuízo_Total',
        'Lucro_Médio_Trade', 'Lucro_%_Médio', 'Prejuízo_Médio_Trade', 'Prejuízo_%_Médio'
    ])

    # ------------------------------------------------------------------------
    # ⏬ SELEÇÃO DE ESTRATÉGIAS ⏬

    dados_candles = baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True)

    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=utBotAlerts,
    #     nome_estrategia = "UT BOTS",
    #     initial_balance=INITIAL_BALANCE,
    #     atr_multiplier=2,
    #     atr_period=1,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageRSIVolumeStrategy,
    #     nome_estrategia = "MA RSI e VOLUME",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # #######################################################################################################
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 7_40- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 7_40",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=7,
    #     slow_window=40,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 5_10- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 5_10",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=5,
    #     slow_window=10,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 5_13- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 5_13",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=5,
    #     slow_window=13,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 7_14- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 7_14",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=7,
    #     slow_window=14,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 8_16- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 8_16",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=8,
    #     slow_window=16,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 10_20- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 10_20",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=10,
    #     slow_window=20,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 9_21 - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 9_21",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=9,
    #     slow_window=21,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 10_50 - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 10_50",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=10,
    #     slow_window=50,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 13_26 - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia = "MA ANTECIPATION 13_26",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=13,
    #     slow_window=26,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)

    # # #######################################################################################################
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=7,
    #     slow_window=40,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 7_40- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 7_40",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=7,
    #     slow_window=40,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 5_10- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 5_10",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=5,
    #     slow_window=10,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 5_13- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 5_13",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=5,
    #     slow_window=13,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 7_14- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 7_14",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=7,
    #     slow_window=14,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 8_16- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 8_16",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=8,
    #     slow_window=16,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 10_20- {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 10_20",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=10,
    #     slow_window=20,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 9_21 - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 9_21",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=9,
    #     slow_window=21,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 10_50 - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 10_50",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=10,
    #     slow_window=50,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 13_26 - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia = "MA SIMPLES FALLBACK 13_26",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=13,
    #     slow_window=26,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # #######################################################################################################
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getRsiTradeStrategy,
    #     nome_estrategia = "RSI",
    #     initial_balance=INITIAL_BALANCE,
    #     low=30,
    #     high=70,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - VORTEX - {str(CANDLE_PERIOD)}")
    # lista = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getVortexTradeStrategy,
    #     nome_estrategia = "VORTEX",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ========================================================================
    print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
    lista = backtestRunner(
        stock_data=dados_candles,
        strategy_function=utBotAlerts,
        nome_estrategia = "UT BOTS",
        initial_balance=INITIAL_BALANCE,
        atr_multiplier=2,
        atr_period=1,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([lista], columns=df.columns)], axis=0, ignore_index=True)
    # ------------------------------------------------------------------------
    print("\n\n")

    # ------------------------------------------------------------------------
    df['Moeda'] = NOME_MOEDA
    df['CANDLE_PERIOD'] = CANDLE_PERIOD
    return df