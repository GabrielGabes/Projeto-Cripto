import pandas as pd

def ichimoku(df, tenkan_period=9, kijun_period=26, senkou_span_b_period=52, displacement=26):
    """
    Calcula o Ichimoku Cloud (Ichimoku Kinko Hyo)
    
    Parâmetros:
    df (pd.DataFrame): DataFrame com dados OHLC
    tenkan_period (int): Período para cálculo do Tenkan-sen (linha de conversão)
    kijun_period (int): Período para cálculo do Kijun-sen (linha base)
    senkou_span_b_period (int): Período para cálculo do Senkou Span B (linha de span B)
    displacement (int): Deslocamento para projetar as linhas futuras
    
    Retorno:
    Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]: (Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, Chikou Span)
    """
    # Determinar máximos e mínimos para os períodos
    high_prices = df['high']
    low_prices = df['low']
    
    # Tenkan-sen (Conversion Line): (highest high + lowest low)/2 for the past 9 periods
    tenkan_sen = (high_prices.rolling(window=tenkan_period).max() + 
                   low_prices.rolling(window=tenkan_period).min()) / 2
    
    # Kijun-sen (Base Line): (highest high + lowest low)/2 for the past 26 periods
    kijun_sen = (high_prices.rolling(window=kijun_period).max() + 
                  low_prices.rolling(window=kijun_period).min()) / 2
                  
    # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2 plotted 26 periods ahead
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(displacement)
    
    # Senkou Span B (Leading Span B): (highest high + lowest low)/2 for the past 52 periods, plotted 26 periods ahead
    senkou_span_b = ((high_prices.rolling(window=senkou_span_b_period).max() + 
                       low_prices.rolling(window=senkou_span_b_period).min()) / 2).shift(displacement)
                       
    # Chikou Span (Lagging Span): Close price plotted 26 periods back
    chikou_span = df['close'].shift(-displacement)
    
    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span