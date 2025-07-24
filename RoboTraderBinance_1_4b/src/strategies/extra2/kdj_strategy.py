import pandas as pd
import numpy as np


def getKDJTradeStrategy(
    stock_data: pd.DataFrame,
    k_period: int = 9, 
    d_period: int = 3,
    j_period: int = 3,
    overbought: int = 80,
    oversold: int = 20,
    verbose: bool = True,
    all_metrics_return: bool = True
):
    """
    Estratégia KDJ (Stochastic Oscillator) para negociação.
    
    - Compra quando a linha K cruza acima da linha D na zona de sobrevenda
    - Venda quando a linha K cruza abaixo da linha D na zona de sobrecompra
    
    Parâmetros:
    - k_period: Período para cálculo do %K
    - d_period: Período para cálculo da média móvel do %K para %D
    - j_period: Período para cálculo do %J
    - overbought: Nível de sobrecompra (normalmente 80)
    - oversold: Nível de sobrevenda (normalmente 20)
    """
    stock_data = stock_data.copy()
    
    # Renomeando colunas para compatibilidade
    if 'high_price' in stock_data.columns:
        stock_data['high'] = stock_data['high_price']
        stock_data['low'] = stock_data['low_price']
        stock_data['close'] = stock_data['close_price']
    
    # Calcular %K (Stochastic)
    low_min = stock_data['low'].rolling(window=k_period).min()
    high_max = stock_data['high'].rolling(window=k_period).max()
    
    stock_data['rsv'] = 100 * ((stock_data['close'] - low_min) / (high_max - low_min))
    
    # Calcular %K, %D, %J
    stock_data['k'] = stock_data['rsv'].rolling(window=d_period).mean()
    stock_data['d'] = stock_data['k'].rolling(window=j_period).mean()
    stock_data['j'] = 3 * stock_data['k'] - 2 * stock_data['d']
    
    # Remover NaN
    stock_data.dropna(subset=['k', 'd', 'j'], inplace=True)
    
    # Verificar se temos dados suficientes
    if len(stock_data) < max(k_period, d_period, j_period):
        if verbose:
            print("⚠️ Dados insuficientes para cálculo do KDJ. Pulando período...")
        return None
    
    # Últimos valores
    last_k = stock_data['k'].iloc[-1]
    prev_k = stock_data['k'].iloc[-2]
    last_d = stock_data['d'].iloc[-1]
    prev_d = stock_data['d'].iloc[-2]
    last_j = stock_data['j'].iloc[-1]
    
    # Detectar cruzamentos
    k_crosses_above_d = prev_k < prev_d and last_k > last_d
    k_crosses_below_d = prev_k > prev_d and last_k < last_d
    
    # Decisão de compra/venda
    buy_condition = k_crosses_above_d and last_k < oversold
    sell_condition = k_crosses_below_d and last_k > overbought
    
    # Se não houver cruzamento, verificar condições extremas
    if not buy_condition and not sell_condition:
        buy_condition = last_j < 0  # J abaixo de zero é um sinal de compra mais agressivo
        sell_condition = last_j > 100  # J acima de 100 é um sinal de venda mais agressivo
    
    trade_decision = True if buy_condition else False if sell_condition else None
    
    if verbose:
        print("-------")
        print("📊 Estratégia: KDJ")
        print(f" | K: {last_k:.2f}")
        print(f" | D: {last_d:.2f}")
        print(f" | J: {last_j:.2f}")
        print(f" | Nível de sobrevenda: {oversold}")
        print(f" | Nível de sobrecompra: {overbought}")
        print(f" | Decisão: {'Comprar' if trade_decision == True else 'Vender' if trade_decision == False else 'Nenhuma'}")
        print("-------")
    
    if all_metrics_return:
        metrics = {
            'open_time_join': stock_data['open_time'],
            'RSV': stock_data['rsv'],
            'K': stock_data['k'],
            'D': stock_data['d'],
            'J': stock_data['j']
        }
        metrics = pd.DataFrame(metrics)
        return trade_decision, metrics
    
    else:
        return trade_decision