from binance.client import Client
import os
from dotenv import load_dotenv

# Carregar chaves da API da Binance (opcional, só é necessário para chamadas privadas)
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

# Inicializar cliente
client = Client(API_KEY, API_SECRET)

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

          
# Obter todos os pares de negociação da Binance
tickers = client.get_exchange_info()['symbols']

# Gerar conjunto de todos os símbolos disponíveis
symbol_set = {item['symbol'] for item in tickers}

# Verificar se cada moeda está listada com par USDT
print("Verificação de moedas na Binance com par USDT:\n")

for moeda in moedas:
    par = f"{moeda}USDT"
    if par in symbol_set:
        print(f"✅ {moeda} está listada (par {par})")
    else:
        print(f"❌ {moeda} NÃO está listada com par USDT")