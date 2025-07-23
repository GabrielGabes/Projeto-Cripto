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

# Extra 2
from strategies.extra2.bollinger_bands_strategy import getBollingerBandsTradeStrategy
from strategies.extra2.ichimoku_strategy import getIchimokuTradeStrategy
from strategies.extra2.kdj_strategy import getKDJTradeStrategy
from strategies.extra2.macd_strategy import getMACDTradeStrategy
from strategies.extra2.stoch_rsi_strategy import getStochRSITradeStrategy
from strategies.extra2.stochastic_rsi_strategy import getStochasticRsiStrategy
from strategies.extra2.supertrend_strategy import getSupertrendTradeStrategy
from strategies.extra2.williams_r_strategy import getWilliamsRTradeStrategy

# Extra
from strategies.extras.accelerator_oscillator_strategy import getAcceleratorOscillatorTradeStrategy
from strategies.extras.alma_strategy import getALMATradeStrategy
from strategies.extras.arnaud_legoux_moving_average_strategy import getArnaudLegouxMovingAverageTradeStrategy
from strategies.extras.aroon_oscillator_strategy import getAroonOscillatorTradeStrategy
from strategies.extras.aroon_strategy import getAroonTradeStrategy
from strategies.extras.atr_strategy import getATRTradeStrategy
from strategies.extras.awesome_oscillator_strategy import getAwesomeOscillatorTradeStrategy
from strategies.extras.chaikin_oscillator_strategy import getChaikinOscillatorTradeStrategy
from strategies.extras.chande_momentum_oscillator_strategy import getChandeMomentumOscillatorTradeStrategy
from strategies.extras.cmf_strategy import getCmfTradeStrategy
from strategies.extras.detrended_price_oscillator_strategy import getDetrendedPriceOscillatorTradeStrategy
from strategies.extras.donchian_channel_strategy import getDonchianChannelTradeStrategy
from strategies.extras.donchian_channels_strategy import getDonchianChannelsTradeStrategy
from strategies.extras.ehler_fisher_transform_strategy import getEhlerFisherTransformTradeStrategy
from strategies.extras.elder_force_index_strategy import getElderForceIndexTradeStrategy
from strategies.extras.elder_ray_strategy import getElderRayTradeStrategy
from strategies.extras.fisher_transform_strategy import getFisherTransformTradeStrategy
from strategies.extras.force_index_strategy import getForceIndexTradeStrategy
from strategies.extras.fractals_strategy import getFractalsTradeStrategy
from strategies.extras.gator_oscillator_strategy import getGatorOscillatorTradeStrategy
from strategies.extras.hilbert_transform_strategy import getHilbertTransformTradeStrategy
from strategies.extras.hull_moving_average_strategy import getHullMovingAverageTradeStrategy
from strategies.extras.ichimoku_cloud_strategy import getIchimokuCloudTradeStrategy
from strategies.extras.kama_strategy import getKAMATradeStrategy
from strategies.extras.keltner_channel_strategy import getKeltnerChannelTradeStrategy
from strategies.extras.keltner_channels_strategy import getKeltnerChannelsTradeStrategy
from strategies.extras.linear_regression_strategy import getLinearRegressionTradeStrategy
from strategies.extras.market_facilitation_index_strategy import getMarketFacilitationIndexTradeStrategy
from strategies.extras.mfi_strategy import getMfiTradeStrategy
from strategies.extras.moving_average_envelope_strategy import getMovingAverageEnvelopeTradeStrategy
from strategies.extras.obv_strategy import getOBVTradeStrategy
from strategies.extras.pivot_points_strategy import getPivotPointsTradeStrategy
from strategies.extras.ppo_strategy import getPPOTradeStrategy
from strategies.extras.price_channels_strategy import getPriceChannelsTradeStrategy
from strategies.extras.psar_strategy import getPSARTradeStrategy
from strategies.extras.roc_strategy import getROCTradeStrategy
from strategies.extras.schaff_trend_cycle_strategy import getSchaffTrendCycleTradeStrategy
from strategies.extras.t3_moving_average_strategy import getT3MovingAverageTradeStrategy
from strategies.extras.tema_strategy import getTEMATradeStrategy
from strategies.extras.time_series_forecast_strategy import getTimeSeriesForecastTradeStrategy
from strategies.extras.triangular_moving_average_strategy import getTriangularMovingAverageTradeStrategy
from strategies.extras.true_strength_index_strategy import getTrueStrengthIndexTradeStrategy
from strategies.extras.ultimate_oscillator_strategy import getUltimateOscillatorTradeStrategy
from strategies.extras.vidya_strategy import getVIDYATradeStrategy
from strategies.extras.volume_weighted_average_price_vwap_strategy import getVolumeWeightedAveragePriceTradeStrategy
from strategies.extras.vwap_strategy import getVolumeWeightedAveragePriceTradeStrategy
from strategies.extras.williams_alligator_strategy import getWilliamsAlligatorTradeStrategy
from strategies.extras.wma_strategy import getWMATradeStrategy
from strategies.extras.zero_lag_moving_average_strategy import getZeroLagMovingAverageTradeStrategy

import time

def backtests_simulador(
        NOME_MOEDA, 
        CANDLE_PERIOD = '1h', 
        DEFAULT_START_DATE='10/07/2025 03:00',
        DEFAULT_END_DATE='20/07/2025 03:00'
        ):
    # ------------------------------------------------------------------------
    # 🔎 AJUSTES BACKTESTS 🔎
    print('#'*100)
    print('MOEDA ANALISADA:', NOME_MOEDA)

    STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
    OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
    INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL
    
    inicio = time.time()
    dados_candles = baixar_candles(OPERATION_CODE, DEFAULT_START_DATE, DEFAULT_END_DATE, CANDLE_PERIOD, ajuste=True)
    fim = time.time()
    tempo_cronometrado = fim - inicio
    print('Tempo baixar_candles (s):', tempo_cronometrado)
    pasta_price_metrics = 'C:/Users/gabri/OneDrive/Documentos/Criptos/Analises/202507/dados_prices_metrics/'
    dados_candles.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '.parquet', index=False)
    # ------------------------------------------------------------------------
    # DATA FRAME PARA CAPTURAR SAIDAS
    df = pd.DataFrame(columns=[
        'Estrategia', 'Data_Inicio', 'Data_Fim', 'Saldo_Final', 'Lucro_%', 'Total_Trades',
        'Trades_Lucrativos', 'Valor_Lucro_Total', 'Trades_Preuízo', 'Valor_Preuízo_Total',
        'Lucro_Médio_Trade', 'Lucro_%_Médio', 'Prejuízo_Médio_Trade', 'Prejuízo_%_Médio'
    ])

    # ------------------------------------------------------------------------
    # ⏬ SELEÇÃO DE ESTRATÉGIAS ⏬

    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - UT BOTS - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'UT BOTS'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=utBotAlerts,
        nome_estrategia="UT BOTS",
        initial_balance=INITIAL_BALANCE,
        atr_multiplier=2,
        atr_period=1,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA RSI e VOLUME - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA RSI e VOLUME '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageRSIVolumeStrategy,
    #     nome_estrategia="MA RSI e VOLUME",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # #######################################################################################################
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 7_40- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 7_40'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 7_40",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=7,
    #     slow_window=40,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 5_10- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 5_10'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 5_10",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=5,
    #     slow_window=10,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 5_13- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 5_13'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 5_13",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=5,
    #     slow_window=13,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 7_14- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 7_14'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 7_14",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=7,
    #     slow_window=14,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 8_16- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 8_16'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 8_16",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=8,
    #     slow_window=16,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 10_20- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 10_20'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 10_20",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=10,
    #     slow_window=20,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 9_21 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 9_21 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 9_21",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=9,
    #     slow_window=21,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 10_50 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 10_50 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 10_50",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=10,
    #     slow_window=50,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA ANTECIPATION 13_26 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA ANTECIPATION 13_26 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageAntecipationTradeStrategy,
    #     nome_estrategia="MA ANTECIPATION 13_26",
    #     initial_balance=INITIAL_BALANCE,
    #     volatility_factor=0.5,
    #     fast_window=13,
    #     slow_window=26,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)

    # # #######################################################################################################
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=7,
    #     slow_window=40,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 7_40- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 7_40'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 7_40",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=7,
    #     slow_window=40,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 5_10- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 5_10'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 5_10",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=5,
    #     slow_window=10,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 5_13- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 5_13'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 5_13",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=5,
    #     slow_window=13,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 7_14- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 7_14'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 7_14",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=7,
    #     slow_window=14,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 8_16- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 8_16'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 8_16",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=8,
    #     slow_window=16,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 10_20- {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 10_20'
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 10_20",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=10,
    #     slow_window=20,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 9_21 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 9_21 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 9_21",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=9,
    #     slow_window=21,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 10_50 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 10_50 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 10_50",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=10,
    #     slow_window=50,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MA SIMPLES FALLBACK 13_26 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MA SIMPLES FALLBACK 13_26 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageTradeStrategy,
    #     nome_estrategia="MA SIMPLES FALLBACK 13_26",
    #     initial_balance=INITIAL_BALANCE,
    #     fast_window=13,
    #     slow_window=26,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # #######################################################################################################
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - RSI - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'RSI'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getRsiTradeStrategy,
        nome_estrategia="RSI",
        initial_balance=INITIAL_BALANCE,
        low=30,
        high=70,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - VORTEX - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'VORTEX '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getVortexTradeStrategy,
    #     nome_estrategia="VORTEX",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ========================================================================

    # print(f"\n{STOCK_CODE} - Bollinger Bands - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Bollinger Bands '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getBollingerBandsTradeStrategy,
    #     nome_estrategia="Bollinger Bands",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Ichimoku - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Ichimoku '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getIchimokuTradeStrategy,
    #     nome_estrategia="Ichimoku",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - KDJ - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'KDJ '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getKDJTradeStrategy,
    #     nome_estrategia="KDJ",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - MACD - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'MACD'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getMACDTradeStrategy,
        nome_estrategia="MACD",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Stochastic RSI - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Stochastic RSI '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getStochRSITradeStrategy,
    #     nome_estrategia="Stochastic RSI",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # falta o indicador
    # # print(f"\n{STOCK_CODE} - Stochastic RSI v2 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- Stochastic RSI v2 '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getStochasticRsiStrategy,
    # #     nome_estrategia="Stochastic RSI v2",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # lento demais
    # # print(f"\n{STOCK_CODE} - Supertrend - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- Supertrend '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getSupertrendTradeStrategy,
    # #     nome_estrategia="Supertrend",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Williams %R - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Williams %R '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getWilliamsRTradeStrategy,
    #     nome_estrategia="Williams %R",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - Accelerator Oscillator - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'Accelerator Oscillator'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getAcceleratorOscillatorTradeStrategy,
        nome_estrategia="Accelerator Oscillator",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - ALMA - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'ALMA '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getALMATradeStrategy,
    #     nome_estrategia="ALMA",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - ALMA Cruzamento (Arnaud Legoux) - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'ALMA Cruzamento (Arnaud Legoux) '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getArnaudLegouxMovingAverageTradeStrategy,
    #     nome_estrategia="ALMA Cruzamento",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Aroon Oscillator - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Aroon Oscillator '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getAroonOscillatorTradeStrategy,
    #     nome_estrategia="Aroon Oscillator",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Aroon Puro - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Aroon Puro '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getAroonTradeStrategy,
    #     nome_estrategia="Aroon Puro",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - ATR - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'ATR '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getATRTradeStrategy,
    #     nome_estrategia="ATR",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Awesome Oscillator - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Awesome Oscillator '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getAwesomeOscillatorTradeStrategy,
    #     nome_estrategia="Awesome Oscillator",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Chaikin Oscillator - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Chaikin Oscillator '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getChaikinOscillatorTradeStrategy,
    #     nome_estrategia="Chaikin Oscillator",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Chande Momentum Oscillator - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Chande Momentum Oscillator '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getChandeMomentumOscillatorTradeStrategy,
    #     nome_estrategia="Chande Momentum Oscillator",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - CMF - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'CMF '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getCmfTradeStrategy,
    #     nome_estrategia="CMF",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Detrended Price Oscillator - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Detrended Price Oscillator '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getDetrendedPriceOscillatorTradeStrategy,
    #     nome_estrategia="Detrended Price Oscillator",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Donchian Channel - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Donchian Channel '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getDonchianChannelTradeStrategy,
    #     nome_estrategia="Donchian Channel",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Donchian Channels v2 - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Donchian Channels v2 '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getDonchianChannelsTradeStrategy,
    #     nome_estrategia="Donchian Channels v2",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # lenta dms
    # # print(f"\n{STOCK_CODE} - Ehlers Fisher Transform - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- Ehlers Fisher Transform '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getEhlerFisherTransformTradeStrategy,
    # #     nome_estrategia="Ehlers Fisher Transform",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Elder Force Index - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Elder Force Index '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getElderForceIndexTradeStrategy,
    #     nome_estrategia="Elder Force Index",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Elder Ray - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Elder Ray '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getElderRayTradeStrategy,
    #     nome_estrategia="Elder Ray",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # lenta dms
    # # print(f"\n{STOCK_CODE} - Fisher Transform - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- Fisher Transform '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getFisherTransformTradeStrategy,
    # #     nome_estrategia="Fisher Transform",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - Force Index - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'Force Index'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getForceIndexTradeStrategy,
        nome_estrategia="Force Index",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Fractals - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Fractals '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getFractalsTradeStrategy,
    #     nome_estrategia="Fractals",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - GATOR OSCILLATOR - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'GATOR OSCILLATOR '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getGatorOscillatorTradeStrategy,
    #     nome_estrategia="GATOR OSCILLATOR",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - HILBERT TRANSFORM - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'HILBERT TRANSFORM '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getHilbertTransformTradeStrategy,
    #     nome_estrategia="HILBERT TRANSFORM",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - ICHIMOKU CLOUD - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'ICHIMOKU CLOUD '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getIchimokuCloudTradeStrategy,
    #     nome_estrategia="ICHIMOKU CLOUD",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - KAMA - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'KAMA '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getKAMATradeStrategy,
    #     nome_estrategia="KAMA",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - KELTNER CHANNEL - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'KELTNER CHANNEL '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getKeltnerChannelTradeStrategy,
    #     nome_estrategia="KELTNER CHANNEL",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - KELTNER CHANNELS - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'KELTNER CHANNELS '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getKeltnerChannelsTradeStrategy,
    #     nome_estrategia="KELTNER CHANNELS",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # lenta dms
    # # print(f"\n{STOCK_CODE} - LINEAR REGRESSION - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- LINEAR REGRESSION '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getLinearRegressionTradeStrategy,
    # #     nome_estrategia="LINEAR REGRESSION",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MARKET FACILITATION INDEX - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MARKET FACILITATION INDEX '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMarketFacilitationIndexTradeStrategy,
    #     nome_estrategia="MARKET FACILITATION INDEX",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - MFI - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'MFI '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMfiTradeStrategy,
    #     nome_estrategia="MFI",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - HULL MOVING AVERAGE - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'HULL MOVING AVERAGE '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getHullMovingAverageTradeStrategy,
    #     nome_estrategia="HULL MOVING AVERAGE",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Moving Average Envelope - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Moving Average Envelope '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getMovingAverageEnvelopeTradeStrategy,
    #     nome_estrategia="Moving Average Envelope",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - OBV - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'OBV '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getOBVTradeStrategy,
    #     nome_estrategia="OBV",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Pivot Points - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Pivot Points '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getPivotPointsTradeStrategy,
    #     nome_estrategia="Pivot Points",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - PPO - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'PPO '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getPPOTradeStrategy,
    #     nome_estrategia="PPO",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Price Channels - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Price Channels '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getPriceChannelsTradeStrategy,
    #     nome_estrategia="Price Channels",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # faltando o indicador
    # # print(f"\n{STOCK_CODE} - PSAR - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- PSAR '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getPSARTradeStrategy,
    # #     nome_estrategia="PSAR",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - ROC - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'ROC '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getROCTradeStrategy,
    #     nome_estrategia="ROC",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Schaff Trend Cycle - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Schaff Trend Cycle '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getSchaffTrendCycleTradeStrategy,
    #     nome_estrategia="Schaff Trend Cycle",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - T3 Moving Average - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'T3 Moving Average '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getT3MovingAverageTradeStrategy,
    #     nome_estrategia="T3 Moving Average",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # # lenta dms
    # # print(f"\n{STOCK_CODE} - Time Series Forecast - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = '- Time Series Forecast '
    # # final_results, price_metrics = backtestRunner(
    # #     stock_data=dados_candles,
    # #     strategy_function=getTimeSeriesForecastTradeStrategy,
    # #     nome_estrategia="Time Series Forecast",
    # #     initial_balance=INITIAL_BALANCE,
    # #     start_date=DEFAULT_START_DATE,
    # #     end_date=DEFAULT_END_DATE,
    # #     verbose=False,
    # # )
    # # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - TEMA - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'TEMA '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getTEMATradeStrategy,
    #     nome_estrategia="TEMA",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - Triangular Moving Average - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'Triangular Moving Average '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getTriangularMovingAverageTradeStrategy,
    #     nome_estrategia="Triangular Moving Average",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # # ------------------------------------------------------------------------
    # print(f"\n{STOCK_CODE} - True Strength Index - {str(CANDLE_PERIOD)}")
    # NOME_ESTRATEGIA = 'True Strength Index '
    # final_results, price_metrics = backtestRunner(
    #     stock_data=dados_candles,
    #     strategy_function=getTrueStrengthIndexTradeStrategy,
    #     nome_estrategia="True Strength Index",
    #     initial_balance=INITIAL_BALANCE,
    #     start_date=DEFAULT_START_DATE,
    #     end_date=DEFAULT_END_DATE,
    #     verbose=False,
    # )
    # df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    # price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - Ultimate Oscillator - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'Ultimate Oscillator'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getUltimateOscillatorTradeStrategy,
        nome_estrategia="Ultimate Oscillator",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - VIDYA - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'VIDYA'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getVIDYATradeStrategy,
        nome_estrategia="VIDYA",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - Volume Weighted Average Price VWAP - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'Weighted Average Price VWAP'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getVolumeWeightedAveragePriceTradeStrategy,
        nome_estrategia="Volume Weighted Average Price VWAP",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - Williams Alligator - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'Williams Alligator'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getWilliamsAlligatorTradeStrategy,
        nome_estrategia="Williams Alligator",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - WMA - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'WMA'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getWMATradeStrategy,
        nome_estrategia="WMA",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print(f"\n{STOCK_CODE} - Zero Lag Moving Average - {str(CANDLE_PERIOD)}")
    NOME_ESTRATEGIA = 'Zero Lag Moving Average'
    final_results, price_metrics = backtestRunner(
        stock_data=dados_candles,
        strategy_function=getZeroLagMovingAverageTradeStrategy,
        nome_estrategia="Zero Lag Moving Average",
        initial_balance=INITIAL_BALANCE,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE,
        verbose=False,
    )
    df = pd.concat([df, pd.DataFrame([final_results], columns=df.columns)], axis=0, ignore_index=True)
    price_metrics.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '_' + NOME_ESTRATEGIA + '.parquet', index=False)
    # ------------------------------------------------------------------------
    print("\n\n")
    # ------------------------------------------------------------------------
    df['Moeda'] = NOME_MOEDA
    df['CANDLE_PERIOD'] = CANDLE_PERIOD
    return df

# df = backtests_simulador(
#         'UNI', 
#         CANDLE_PERIOD = '1h', 
#         DEFAULT_START_DATE='12/03/2025 03:00',
#         DEFAULT_END_DATE='15/03/2025 03:00'
#         )
# pasta_salvar = 'C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/tests/graficos/'
# df.to_parquet(pasta_salvar + 'DADOS_SIMULADOS_1semana_extra.parquet', index=False)
# df = pd.read_parquet(pasta_salvar + 'DADOS_SIMULADOS_1semana_extra.parquet')
# df.head().T