# BIBLIOTECAS EXTRAS
import sys
sys.path.append("C:/Users/gabri/OneDrive/Documentos/PROJETOS PARADOS OU TERMINADOS/RoboTraderBinance_1_4 - Copia/src")

from tests.calculadora_candles import calculadora_candles
from tests.backtests_simulador import backtests_simulador
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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
df_final = pd.DataFrame(columns = [
    'Balanço final', 'Lucro/prejuízo percentual', 'Total de operações',
    'ESTRATÉGIA', 'Moeda', 'CANDLE_PERIOD', 'CLANDES_RODADOS',
    'TEMPO_RODANDO'
    ])

moedas = ['BTC','ETH','XRP','SOL','BNB',
          'DOGE','ADA','TRX','LINK','AVAX',
          'PEPE','SHIB']
periodos = [
            # MINUTOS
            Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_3MINUTE, Client.KLINE_INTERVAL_5MINUTE, 
            Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE, 
            # HORAS
            Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_4HOUR, 
            Client.KLINE_INTERVAL_6HOUR, Client.KLINE_INTERVAL_8HOUR, Client.KLINE_INTERVAL_12HOUR, 
            # DIA # SEMANA
            Client.KLINE_INTERVAL_1DAY, Client.KLINE_INTERVAL_1WEEK
            ]
tipos_saida = ['dia','semana','mes']

for moeda in moedas:
    for periodo in periodos:
        for tipo_saida in tipos_saida:
            df_temp = backtests_simulador(moeda, periodo, tipo_saida)
            df_temp['TEMPO_RODANDO'] = tipo_saida
            df_final = pd.concat([df_final, df_temp], axis=0, ignore_index=True)


print('*'*30, 'TERMINOU DE RODAR', '*'*30)
df_final.to_excel('DADOS_SIMULADOS.xlsx', index=False)
df_final.shape