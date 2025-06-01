import pandas as pd
import numpy as np


def getBollingerBandsTradeStrategy(
    stock_data: pd.DataFrame,
    window: int = 20,
    num_std: float = 2.0,
    verbose: bool = True
):
    """
    Estratégia de Bandas de Bollinger para negociação.
    
    - Compra quando o preço toca ou cruza abaixo da banda inferior
    - Venda quando o preço toca ou cruza acima da banda superior
    
    Parâmetros:
    - window: Período para a média móvel (normalmente 20)
    - num_std: Número de desvios padrão para as bandas (normalmente 2)
    """
    stock_data = stock_data.copy()
    
    # Calcular Bandas de Bollinger
    stock_data['middle_band'] = stock_data['close_price'].rolling(window=window).mean()
    std_dev = stock_data['close_price'].rolling(window=window).std()
    
    stock_data['upper_band'] = stock_data['middle_band'] + (std_dev * num_std)
    stock_data['lower_band'] = stock_data['middle_band'] - (std_dev * num_std)
    
    # Remover NaN
    stock_data.dropna(subset=['middle_band', 'upper_band', 'lower_band'], inplace=True)
    
    # Verificar se temos dados suficientes
    if len(stock_data) < window:
        if verbose:
            print("⚠️ Dados insuficientes para cálculo das Bandas de Bollinger. Pulando período...")
        return None
    
    # Últimos valores
    last_close = stock_data['close_price'].iloc[-1]
    last_upper = stock_data['upper_band'].iloc[-1]
    last_lower = stock_data['lower_band'].iloc[-1]
    last_middle = stock_data['middle_band'].iloc[-1]
    
    # Calcular onde o preço está em relação às bandas (% B)
    # %B = (Close - Lower Band) / (Upper Band - Lower Band)
    percent_b = (last_close - last_lower) / (last_upper - last_lower)
    
    # Decisão de compra/venda
    buy_condition = percent_b <= 0.05  # Preço está muito próximo ou abaixo da banda inferior
    sell_condition = percent_b >= 0.95  # Preço está muito próximo ou acima da banda superior
    
    trade_decision = True if buy_condition else False if sell_condition else None
    
    if verbose:
        print("-------")
        print("📊 Estratégia: Bandas de Bollinger")
        print(f" | Preço atual: {last_close:.6f}")
        print(f" | Banda superior: {last_upper:.6f}")
        print(f" | Banda média: {last_middle:.6f}")
        print(f" | Banda inferior: {last_lower:.6f}")
        print(f" | %B: {percent_b:.2f}")
        print(f" | Decisão: {'Comprar' if trade_decision == True else 'Vender' if trade_decision == False else 'Nenhuma'}")
        print("-------")
    
    return trade_decision