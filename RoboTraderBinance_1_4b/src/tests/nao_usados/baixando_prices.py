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

import pandas as pd
import time

from binance.client import Client
from tests.baixar_candles import baixar_candles
# ------------------------------------------------------------------------
# DATA FRAME PARA CAPTURAR SAIDAS
df = pd.DataFrame(columns=[
    'Estrategia', 'Data_Inicio', 'Data_Fim', 'Saldo_Final', 'Lucro_%', 'Total_Trades',
    'Trades_Lucrativos', 'Valor_Lucro_Total', 'Trades_Preuízo', 'Valor_Preuízo_Total',
    'Lucro_Médio_Trade', 'Lucro_%_Médio', 'Prejuízo_Médio_Trade', 'Prejuízo_%_Médio'
    ])

moedas = [
    # TOP 29 MOEDAS ## 04/06/2025
    'BTC', # Bitcoin
    'ETH', # Ethereum
    'XRP', # XRP
    'BNB', # BNB
    'SOL', # Solana
    'DOGE', # Dogecoin
    'TRX', # TRON
    'ADA', # Cardano
    'SUI', # Sui
    'LINK', # Chainlink
    'AVAX', # Avalanche
    'XLM', # Stellar
    'BCH', # Bitcoin Cash
    'TON', # Toncoin
    'SHIB', # Shiba Inu
    'HBAR', # Hedera
    'LTC', # Litecoin
    'DOT', # Polkadot
    'XMR', # Monero
    'PEPE', # Pepe
    'AAVE', # Aave
    'UNI', # Uniswap
    'TAO', # Bittensor
    'APT', # Aptos
    'NEAR', # NEAR Protocol
    'ICP', # Internet Computer
    'ONDO', # Ondo
    'ETC', # Ethereum Classic
    'POL', # POL (prev. MATIC)
    'USD1', # World Liberty Financial USD
    'TRUMP', # OFFICIAL TRUMP
    'VET', # VeChain
    'RENDER', # Render
    'FET', # Artificial Superintelligence Alliance
    'ENA', # Ethena
    'WLD', # Worldcoin
    'ARB', # Arbitrum

    ## TOP MOEDAS BOAS E FORA DOS HOLOFOTES ##
    'ALGO', # Algorand
    'NEAR', # Near Protocol
    'FLOW', # Flow
    'KDA', # Kadena
    'HBAR', # Hedera Hashgraph
    'ROSE', # Oasis Network
    'OCEAN', # Ocean Protocol
    'AR', # Arweave
    'CELO', # Celo
    'SCRT' # Secret Network
          ]
CANDLE_PERIOD = Client.KLINE_INTERVAL_15MINUTE

count = 0
# Rodando simulação para cada moeda
for NOME_MOEDA in moedas:
    print('#'*100)
    print('MOEDA BAIXADA:', NOME_MOEDA)

    STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
    OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
    
    inicio = time.time()
    dados_candles = baixar_candles(OPERATION_CODE, '22/12/2024 00:00', '23/07/2025 01:30', CANDLE_PERIOD, ajuste=True)
    fim = time.time()
    tempo_cronometrado = fim - inicio
    print('Tempo baixar_candles (s):', tempo_cronometrado)
    pasta_price_metrics = 'C:/Users/gabri/OneDrive/Documentos/Criptos/Analises/202507/dados_prices_metrics/'
    dados_candles.to_parquet(pasta_price_metrics + NOME_MOEDA + '_' + CANDLE_PERIOD + '.parquet', index=False)

print('='*35, 'FIM', '='*35)