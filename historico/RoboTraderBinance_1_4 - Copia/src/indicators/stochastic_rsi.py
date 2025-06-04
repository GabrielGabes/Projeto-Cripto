import pandas as pd
from .rsi import rsi

def stochastic_rsi(series, rsi_period=14, stoch_period=14, k_period=3, d_period=3):
    """
    Calcula o Stochastic RSI
    
    Parâmetros:
    series (pd.Series): Série de preços de fechamento
    rsi_period (int): Período para cálculo do RSI
    stoch_period (int): Período para cálculo do Stochastic
    k_period (int): Período para suavização da linha K
    d_period (int): Período para cálculo da linha D
    
    Retorno:
    Tuple[pd.Series, pd.Series]: (K%, D%)
    """
    # Primeiro calcular o RSI
    rsi_values = pd.Series(rsi(series, rsi_period, False))
    
    # Calcular o Stochastic a partir do RSI
    lowest_rsi = rsi_values.rolling(window=stoch_period).min()
    highest_rsi = rsi_values.rolling(window=stoch_period).max()
    
    # Evita divisão por zero
    denominator = highest_rsi - lowest_rsi
    denominator = denominator.replace(0, 0.000001)
    
    # Cálculo do K% (linha principal do Stochastic)
    k = 100 * ((rsi_values - lowest_rsi) / denominator)
    
    # Suavização da linha K
    k_smooth = k.rolling(window=k_period).mean()
    
    # Média móvel simples do K% para obter D% (linha de sinal)
    d = k_smooth.rolling(window=d_period).mean()
    
    return k_smooth, d