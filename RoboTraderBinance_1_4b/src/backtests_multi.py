# BIBLIOTECAS EXTRAS
import sys
import getpass # Verificando qual usuario esta executando o codigo
if getpass.getuser() == 'gabri': 
    print('g')
    sys.path.append(r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src")
elif getpass.getuser() == 'michael':
    print('m')
    sys.path.append(r"C:\Users\michael\OneDrive\Documentos\GitHub\Projeto-Cripto\RoboTraderBinance_1_4b\src")
    
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from binance.client import Client
import pandas as pd
from tests.backtests_simulador import backtests_simulador
# ------------------------------------------------------------------------
# DATA FRAME PARA CAPTURAR SAIDAS
df = pd.DataFrame(columns=[
    'Estrategia', 'Data_Inicio', 'Data_Fim', 'Saldo_Final', 'Lucro_%', 'Total_Trades',
    'Trades_Lucrativos', 'Valor_Lucro_Total', 'Trades_Preuízo', 'Valor_Preuízo_Total',
    'Lucro_Médio_Trade', 'Lucro_%_Médio', 'Prejuízo_Médio_Trade', 'Prejuízo_%_Médio',
    'Tempo_Simulacao'
    ])

moedas = [
    # TOP 29 MOEDAS ## 04/06/2025
    'BTC', # Bitcoin
    # 'ETH', # Ethereum
    # 'XRP', # XRP
    # 'BNB', # BNB
    # 'SOL', # Solana
    # 'DOGE', # Dogecoin
    # 'TRX', # TRON
    # 'ADA', # Cardano
    # 'SUI', # Sui
    # 'LINK', # Chainlink
    # 'AVAX', # Avalanche
    # 'XLM', # Stellar
    # 'BCH', # Bitcoin Cash
    # 'TON', # Toncoin
    # 'SHIB', # Shiba Inu
    # 'HBAR', # Hedera
    # 'LTC', # Litecoin
    # 'DOT', # Polkadot
    # 'XMR', # Monero
    # 'PEPE', # Pepe
    # 'AAVE', # Aave
    # 'UNI', # Uniswap
    # 'TAO', # Bittensor
    # 'APT', # Aptos
    # 'NEAR', # NEAR Protocol
    # 'ICP', # Internet Computer
    # 'ONDO', # Ondo
    # 'ETC', # Ethereum Classic
    # 'POL', # POL (prev. MATIC)
    # 'USD1', # World Liberty Financial USD
    # 'VET', # VeChain
    # 'RENDER', # Render
    # 'FET', # Artificial Superintelligence Alliance
    # 'ENA', # Ethena
    # 'WLD', # Worldcoin
    # 'ARB', # Arbitrum

    # ## TOP MOEDAS BOAS E FORA DOS HOLOFOTES ##
    # 'ALGO', # Algorand
    # 'NEAR', # Near Protocol
    # 'FLOW', # Flow
    # 'KDA', # Kadena
    # 'HBAR', # Hedera Hashgraph
    # 'ROSE', # Oasis Network
    # 'OCEAN', # Ocean Protocol
    # 'AR', # Arweave
    # 'CELO', # Celo
    # 'SCRT' # Secret Network
          ]
periodos_candles = [
            # MINUTOS
            # # Periodos muito muito curtos
            # Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_3MINUTE, 
            # Client.KLINE_INTERVAL_5MINUTE, 
            Client.KLINE_INTERVAL_15MINUTE, 
            # Client.KLINE_INTERVAL_30MINUTE, 
            
            # HORAS
            # Client.KLINE_INTERVAL_1HOUR
            # # Periodos muito muito longo
            # , Client.KLINE_INTERVAL_2HOUR, Client.KLINE_INTERVAL_4HOUR, Client.KLINE_INTERVAL_6HOUR, Client.KLINE_INTERVAL_8HOUR, Client.KLINE_INTERVAL_12HOUR,
            
            # DIA # SEMANA
            # Client.KLINE_INTERVAL_1DAY, Client.KLINE_INTERVAL_1WEEK
            ]

from tests.geradores_de_amostras.dom_sab import gerar_domingo_sabado_semanas_ano
# intervalos_tempo = gerar_domingo_sabado_semanas_ano()
# intervalos_tempo = [['22/12/2024 00:00', '23/07/2025 20:30']]
intervalos_tempo = [['01/03/2025 00:00','02/03/2025 01:00'],
                    ['01/03/2025 00:00','03/03/2025 02:00'],
                    ['01/03/2025 00:00','04/03/2025 03:00'],
                    ['01/03/2025 00:00','05/03/2025 04:00'],
                    ['01/03/2025 00:00','06/03/2025 05:00'],
                    ['01/03/2025 00:00','07/03/2025 06:00'],
                    ['01/03/2025 00:00','08/03/2025 07:00'],
                    ['01/03/2025 00:00','09/03/2025 08:00']]

count = 0
# Rodando simulação para cada moeda
for moeda in moedas:
    # para cada periodo de candle
    for periodo in periodos_candles:

        # para cada intervalo de data hora        
        for horarios_lista in intervalos_tempo:

            # Rodando finalmente simulação
            df_temp = backtests_simulador(moeda, periodo, horarios_lista[0], horarios_lista[1])
            df = pd.concat([df, df_temp], axis=0, ignore_index=True) # concatenando no dataframe principal
    
    print(pd.concat([df.head(), df.tail()], axis=0))
    pasta_salvar = 'C:/Users/gabri/OneDrive/Documentos/Criptos/Analises/202507/dados_prices_metrics/'
    df.to_parquet(pasta_salvar + 'DADOS_SIMULADOS_TESTE.parquet', index=False)
    # count += 1
    # if count % 2 == 0:
    #     pasta_salvar = 'C:/Users/gabri/OneDrive/Documentos/Criptos/Analises/202507/dados_prices_metrics/'
        # df.to_parquet(pasta_salvar + 'DADOS_SIMULADOS_20241222a20250723_15m.parquet', index=False)

print('*'*50, 'TERMINOU DE RODAR', '*'*50)
print(df.shape)

# # Remove timezone de todas as colunas datetime com tz-aware # caso for salvar como xlsx
# for col in df.select_dtypes(include=['datetimetz']).columns:
#     df[col] = df[col].dt.tz_localize(None)

pasta_salvar = 'C:/Users/gabri/OneDrive/Documentos/Criptos/Analises/202507/dados_prices_metrics/'
# df.to_parquet(pasta_salvar + 'DADOS_SIMULADOS_20241222a20250723_15m.parquet', index=False)
df.to_parquet(pasta_salvar + 'DADOS_SIMULADOS_TESTE.parquet', index=False)