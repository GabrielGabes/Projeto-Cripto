import pandas as pd
import numpy as np


def getStochRSITradeStrategy(
    stock_data: pd.DataFrame,
    rsi_period: int = 14,
    stoch_period: int = 14,
    k_period: int = 3,
    d_period: int = 3,
    overbought: int = 80,
    oversold: int = 20,
    verbose: bool = True
):
    """
    Estratégia Stochastic RSI - combina RSI e Stochastic.
    
    - Compra quando %K cruza acima de %D na zona de sobrevenda
    - Venda quando %K cruza abaixo de %D na zona de sobrecompra
    """
    from indicators.Indicators import Indicators
    
    stock_data = stock_data.copy()
    
    # Calculate RSI
    delta = stock_data['close_price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Calculate Stochastic RSI
    rsi_min = rsi.rolling(window=stoch_period).min()
    rsi_max = rsi.rolling(window=stoch_period).max()
    stoch_rsi = 100 * (rsi - rsi_min) / (rsi_max - rsi_min)
    
    # Calculate %K and %D
    stock_data['k'] = stoch_rsi.rolling(window=k_period).mean()
    stock_data['d'] = stock_data['k'].rolling(window=d_period).mean()
    
    # Remove NaN values
    stock_data.dropna(subset=['k', 'd'], inplace=True)
    
    if len(stock_data) < max(rsi_period, stoch_period):
        if verbose:
            print("⚠️ Dados insuficientes após remoção de NaN. Pulando período...")
        return None
    
    # Get latest values
    last_k = stock_data['k'].iloc[-1]
    last_d = stock_data['d'].iloc[-1]
    prev_k = stock_data['k'].iloc[-2]
    prev_d = stock_data['d'].iloc[-2]
    
    # Generate signals
    k_crosses_above_d = (last_k > last_d) and (prev_k <= prev_d)
    k_crosses_below_d = (last_k < last_d) and (prev_k >= prev_d)
    
    buy_condition = k_crosses_above_d and (last_k < oversold)
    sell_condition = k_crosses_below_d and (last_k > overbought)
    
    trade_decision = True if buy_condition else False if sell_condition else None
    
    if verbose:
        print("-------")
        print("📊 Estratégia: Stochastic RSI")
        print(f" | Último %K: {last_k:.3f}")
        print(f" | Último %D: {last_d:.3f}")
        print(f" | Nível de Sobrecompra: {overbought}")
        print(f" | Nível de Sobrevenda: {oversold}")
        print(f' | Decisão: {"Comprar" if trade_decision == True else "Vender" if trade_decision == False else "Nenhuma"}')
        print("-------")
    
    return trade_decision

Stochastic_RSI = getStochRSITradeStrategy
StochasticRSI = getStochRSITradeStrategy 