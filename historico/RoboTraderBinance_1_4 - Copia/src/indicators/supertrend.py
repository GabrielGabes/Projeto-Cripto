import pandas as pd
import numpy as np
from .atr import atr

def supertrend(df, atr_period=10, multiplier=3.0):
    """
    Calcula o indicador Supertrend
    
    Parâmetros:
    df (pd.DataFrame): DataFrame com dados OHLC
    atr_period (int): Período para cálculo do ATR
    multiplier (float): Multiplicador para bandas (sensibilidade)
    
    Retorno:
    Tuple[pd.Series, pd.Series]: (Supertrend, Direção da Tendência)
    """
    # Calcula o ATR
    atr_val = atr(df, atr_period)
    
    # Cálculo do Supertrend
    hl2 = (df['high'] + df['low']) / 2
    
    # Basic upper and lower bands
    up = hl2 + (multiplier * atr_val)
    dn = hl2 - (multiplier * atr_val)
    
    # Inicializa séries para armazenar os valores calculados
    trend = pd.Series(np.nan, index=df.index)
    supertrend = pd.Series(np.nan, index=df.index)
    
    # Inicialização
    trend.iloc[0] = 1  # Tendência inicial (1 para alta, -1 para baixa)
    supertrend.iloc[0] = up.iloc[0]  # Valor inicial 
    
    # Calculando o Supertrend
    for i in range(1, len(df)):
        if df['close'].iloc[i-1] <= supertrend.iloc[i-1]:
            trend.iloc[i] = -1  # Downtrend
        else:
            trend.iloc[i] = 1   # Uptrend
            
        # Atualiza bandas baseadas na tendência
        if trend.iloc[i] == 1:
            supertrend.iloc[i] = max(up.iloc[i], supertrend.iloc[i-1])
        else:
            supertrend.iloc[i] = min(dn.iloc[i], supertrend.iloc[i-1])
            
        # Verifica por cruzamentos
        if (df['close'].iloc[i] <= supertrend.iloc[i] and df['close'].iloc[i-1] > supertrend.iloc[i-1]):
            trend.iloc[i] = -1  # Cruzamento para baixo
        elif (df['close'].iloc[i] >= supertrend.iloc[i] and df['close'].iloc[i-1] < supertrend.iloc[i-1]):
            trend.iloc[i] = 1   # Cruzamento para cima
            
        # Atualiza novamente o supertrend
        if trend.iloc[i] == 1:
            supertrend.iloc[i] = max(up.iloc[i], supertrend.iloc[i-1])
        else:
            supertrend.iloc[i] = min(dn.iloc[i], supertrend.iloc[i-1])
    
    return supertrend, trend