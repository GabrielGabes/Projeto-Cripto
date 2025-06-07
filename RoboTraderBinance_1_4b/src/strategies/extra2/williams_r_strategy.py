import pandas as pd
import numpy as np

def getWilliamsRTradeStrategy(
    stock_data: pd.DataFrame,
    period: int = 14,
    overbought: float = -20,
    oversold: float = -80,
    verbose: bool = True
):
    """
    Estratégia Williams %R para negociação.
    
    - Compra quando o Williams %R cruza acima do nível de sobrevenda (oversold)
    - Venda quando o Williams %R cruza abaixo do nível de sobrecompra (overbought)
    
    Parâmetros:
    - period: Período para cálculo do Williams %R
    - overbought: Nível de sobrecompra (normalmente -20)
    - oversold: Nível de sobrevenda (normalmente -80)
    """
    stock_data = stock_data.copy()
    
    # Renomeando colunas para compatibilidade
    if 'high_price' in stock_data.columns:
        stock_data['high'] = stock_data['high_price']
        stock_data['low'] = stock_data['low_price']
        stock_data['close'] = stock_data['close_price']
    
    # Calcular Williams %R
    highest_high = stock_data['high'].rolling(window=period).max()
    lowest_low = stock_data['low'].rolling(window=period).min()
    
    # %R = -100 * ((highest_high - close) / (highest_high - lowest_low))
    stock_data['williams_r'] = -100 * ((highest_high - stock_data['close']) / (highest_high - lowest_low))
    
    # Remover NaN
    stock_data.dropna(subset=['williams_r'], inplace=True)
    
    # Verificar se temos dados suficientes
    if len(stock_data) < period:
        if verbose:
            print("⚠️ Dados insuficientes para cálculo do Williams %R. Pulando período...")
        return None
    
    # Último valor do Williams %R
    last_r = stock_data['williams_r'].iloc[-1]
    previous_r = stock_data['williams_r'].iloc[-2]
    
    # Decisão de compra/venda
    buy_condition = previous_r <= oversold and last_r > oversold
    sell_condition = previous_r >= overbought and last_r < overbought
    
    # Caso não haja cruzamento, verificar a posição atual em relação aos níveis
    if not buy_condition and not sell_condition:
        if last_r < oversold:
            # No território de sobrevenda, sinal potencial de compra
            buy_condition = True
        elif last_r > overbought:
            # No território de sobrecompra, sinal potencial de venda
            sell_condition = True
    
    trade_decision = True if buy_condition else False if sell_condition else None
    
    if verbose:
        print("-------")
        print("📊 Estratégia: Williams %R")
        print(f" | Período: {period}")
        print(f" | Último valor: {last_r:.2f}")
        print(f" | Nível de sobrevenda (oversold): {oversold}")
        print(f" | Nível de sobrecompra (overbought): {overbought}")
        print(f" | Decisão: {'Comprar' if trade_decision == True else 'Vender' if trade_decision == False else 'Nenhuma'}")
        print("-------")
    
    return trade_decision

Williams_R = getWilliamsRTradeStrategy