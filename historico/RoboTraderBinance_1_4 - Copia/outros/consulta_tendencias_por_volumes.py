import ccxt

# Conectar à Binance
binance = ccxt.binance()

def fetch_recent_volumes(symbol, timeframe='1h', limit=3):
    """ Obtém os últimos volumes APENAS dos candles verdes. """
    try:
        candles = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        # Filtrar apenas candles verdes (onde o fechamento > abertura)
        green_volumes = [candle[5] for candle in candles if candle[4] > candle[1]]  # Volume (índice 5), Close (índice 4), Open (índice 1)
        
        return green_volumes if len(green_volumes) >= 3 else []  # Garantimos que pelo menos 3 candles sejam verdes
    except Exception as e:
        print(f"Erro ao buscar volumes para {symbol}: {e}")
        return []

def is_strong_buying_trend(volumes):
    """
    Verifica se:
    1. Os volumes estão em tendência de alta (V1 < V2 < V3)
    2. A soma dos dois últimos volumes é pelo menos 4 vezes maior que o primeiro volume ((V2 + V3) >= 4 * V1)
    """
    if len(volumes) == 3 and volumes[0] < volumes[1] < volumes[2]:
        return (volumes[1] + volumes[2]) >= 4 * volumes[0]
    return False

def get_usdt_pairs():
    """ Obtém todos os ativos que terminam em /USDT e estão ativos na Binance Spot. """
    try:
        markets = binance.load_markets()
        
        # Filtrar apenas pares USDT que estejam ativos para negociação
        usdt_pairs = [
            symbol for symbol, details in markets.items()
            if symbol.endswith('/USDT') and details.get('active', False) and details.get('spot', False)
        ]
        
        return usdt_pairs
    except Exception as e:
        print(f"Erro ao carregar pares da Binance: {e}")
        return []

# Buscar ativos e volumes
usdt_pairs = get_usdt_pairs()
selected_assets = {}

for symbol in usdt_pairs:
    volumes = fetch_recent_volumes(symbol)
    
    if volumes and is_strong_buying_trend(volumes):
        selected_assets[symbol] = volumes

# Exibir resultados
if selected_assets:
    print("Ativos com forte tendência de compra:")
    for symbol, volumes in selected_assets.items():
        print(f"{symbol}: {volumes}")
else:
    print("Nenhum ativo encontrado com forte tendência de compra.")
