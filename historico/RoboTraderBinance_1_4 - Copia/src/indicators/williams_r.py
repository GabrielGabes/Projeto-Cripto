import pandas as pd

def williams_r(df, period=14):
    """
    Calcula o Williams %R
    
    Parâmetros:
    df (pd.DataFrame): DataFrame com dados OHLC
    period (int): Período para cálculo
    
    Retorno:
    pd.Series: Valores do Williams %R
    """
    highest_high = df['high'].rolling(window=period).max()
    lowest_low = df['low'].rolling(window=period).min()
    
    # Evita divisão por zero
    denominator = highest_high - lowest_low
    denominator = denominator.replace(0, 0.000001)
    
    williams_r = ((highest_high - df['close']) / denominator) * -100
    
    return williams_r