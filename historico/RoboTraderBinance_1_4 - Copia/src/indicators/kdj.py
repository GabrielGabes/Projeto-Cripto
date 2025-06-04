import pandas as pd

def kdj(df, k_period=9, d_period=3, j_period=3):
    """
    Calcula o indicador KDJ
    
    Parâmetros:
    df (pd.DataFrame): DataFrame com dados OHLC
    k_period (int): Período para cálculo do K
    d_period (int): Período para cálculo do D
    j_period (int): Período para cálculo do J
    
    Retorno:
    Tuple[pd.Series, pd.Series, pd.Series]: (K, D, J)
    """
    # Cálculo do %K (RSV - Raw Stochastic Value)
    low_min = df['low'].rolling(window=k_period).min()
    high_max = df['high'].rolling(window=k_period).max()
    
    # Evita divisão por zero
    denominator = high_max - low_min
    denominator = denominator.replace(0, 0.000001)
    
    rsv = 100 * ((df['close'] - low_min) / denominator)
    
    # Cálculo do K (primeira suavização do RSV)
    k = pd.Series(0.0, index=df.index)
    k[0] = 50.0  # valor inicial
    for i in range(1, len(df)):
        k[i] = (2/3) * k[i-1] + (1/3) * rsv[i]
    
    # Cálculo do D (segunda suavização)
    d = pd.Series(0.0, index=df.index)
    d[0] = 50.0  # valor inicial
    for i in range(1, len(df)):
        d[i] = (2/3) * d[i-1] + (1/3) * k[i]
    
    # Cálculo do J
    j = 3 * k - 2 * d
    
    return k, d, j