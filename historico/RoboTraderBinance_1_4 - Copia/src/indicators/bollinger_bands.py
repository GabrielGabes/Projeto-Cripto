import pandas as pd

def bollinger_bands(series, window=20, num_std=2.0):
    """
    Calcula as Bandas de Bollinger
    
    Parâmetros:
    series (pd.Series): Série de preços de fechamento
    window (int): Período para cálculo da média móvel
    num_std (float): Número de desvios-padrão para as bandas
    
    Retorno:
    Tuple[pd.Series, pd.Series, pd.Series]: (Banda Superior, Média Móvel, Banda Inferior)
    """
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return upper_band, sma, lower_band