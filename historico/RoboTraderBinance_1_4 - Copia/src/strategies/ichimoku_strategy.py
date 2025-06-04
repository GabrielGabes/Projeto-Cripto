import pandas as pd
import numpy as np


def getIchimokuTradeStrategy(
    stock_data: pd.DataFrame,
    tenkan_period: int = 9,
    kijun_period: int = 26,
    senkou_span_b_period: int = 52,
    displacement: int = 26,
    verbose: bool = True
):
    """
    Estratégia Ichimoku Kinko Hyo para negociação.
    
    - Compra quando o preço cruza acima da nuvem e Tenkan-sen cruza acima de Kijun-sen
    - Venda quando o preço cruza abaixo da nuvem e Tenkan-sen cruza abaixo de Kijun-sen
    
    Parâmetros:
    - tenkan_period: Período para Tenkan-sen (Linha de Conversão)
    - kijun_period: Período para Kijun-sen (Linha de Base)
    - senkou_span_b_period: Período para Senkou Span B
    - displacement: Deslocamento para Senkou Span A/B (Kumo/Nuvem)
    """
    stock_data = stock_data.copy()
    
    # Renomeando colunas para compatibilidade
    if 'high_price' in stock_data.columns:
        stock_data['high'] = stock_data['high_price']
        stock_data['low'] = stock_data['low_price']
        stock_data['close'] = stock_data['close_price']
    
    # Calcular Tenkan-sen (Linha de Conversão)
    tenkan_high = stock_data['high'].rolling(window=tenkan_period).max()
    tenkan_low = stock_data['low'].rolling(window=tenkan_period).min()
    stock_data['tenkan_sen'] = (tenkan_high + tenkan_low) / 2
    
    # Calcular Kijun-sen (Linha de Base)
    kijun_high = stock_data['high'].rolling(window=kijun_period).max()
    kijun_low = stock_data['low'].rolling(window=kijun_period).min()
    stock_data['kijun_sen'] = (kijun_high + kijun_low) / 2
    
    # Calcular Senkou Span A (Linha Principal)
    stock_data['senkou_span_a'] = ((stock_data['tenkan_sen'] + stock_data['kijun_sen']) / 2).shift(displacement)
    
    # Calcular Senkou Span B (Linha de Suporte)
    senkou_high = stock_data['high'].rolling(window=senkou_span_b_period).max()
    senkou_low = stock_data['low'].rolling(window=senkou_span_b_period).min()
    stock_data['senkou_span_b'] = ((senkou_high + senkou_low) / 2).shift(displacement)
    
    # Calcular Chikou Span (Linha Atrasada)
    stock_data['chikou_span'] = stock_data['close'].shift(-displacement)
    
    # Remover NaN
    stock_data.dropna(subset=['tenkan_sen', 'kijun_sen'], inplace=True)
    
    # Verificar se temos dados suficientes
    min_periods = max(tenkan_period, kijun_period, senkou_span_b_period)
    if len(stock_data) < min_periods + displacement:
        if verbose:
            print("⚠️ Dados insuficientes para cálculo do Ichimoku. Pulando período...")
        return None
    
    # Últimos valores
    current_close = stock_data['close'].iloc[-1]
    current_tenkan = stock_data['tenkan_sen'].iloc[-1]
    current_kijun = stock_data['kijun_sen'].iloc[-1]
    
    # Para verificar a posição em relação à nuvem, olhamos para trás no deslocamento
    idx = -displacement if len(stock_data) > displacement else -1
    current_senkou_a = stock_data['senkou_span_a'].iloc[idx]
    current_senkou_b = stock_data['senkou_span_b'].iloc[idx]
    
    # Cruzamentos
    tenkan_above_kijun = current_tenkan > current_kijun
    price_above_cloud = current_close > max(current_senkou_a, current_senkou_b)
    price_below_cloud = current_close < min(current_senkou_a, current_senkou_b)
    
    # Detectar cruzamentos recentes
    prev_tenkan = stock_data['tenkan_sen'].iloc[-2]
    prev_kijun = stock_data['kijun_sen'].iloc[-2]
    tenkan_crossing_up = prev_tenkan <= prev_kijun and current_tenkan > current_kijun
    tenkan_crossing_down = prev_tenkan >= prev_kijun and current_tenkan < current_kijun
    
    # Decisão de compra/venda
    buy_condition = (price_above_cloud and tenkan_above_kijun) or tenkan_crossing_up
    sell_condition = (price_below_cloud and not tenkan_above_kijun) or tenkan_crossing_down
    
    trade_decision = True if buy_condition else False if sell_condition else None
    
    if verbose:
        print("-------")
        print("📊 Estratégia: Ichimoku Kinko Hyo")
        print(f" | Preço atual: {current_close:.6f}")
        print(f" | Tenkan-sen: {current_tenkan:.6f}")
        print(f" | Kijun-sen: {current_kijun:.6f}")
        print(f" | Senkou Span A: {current_senkou_a:.6f}")
        print(f" | Senkou Span B: {current_senkou_b:.6f}")
        print(f" | Posição: {'Acima da nuvem' if price_above_cloud else 'Abaixo da nuvem' if price_below_cloud else 'Dentro da nuvem'}")
        print(f" | Decisão: {'Comprar' if trade_decision == True else 'Vender' if trade_decision == False else 'Nenhuma'}")
        print("-------")
    
    return trade_decision