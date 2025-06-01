import pandas as pd
import numpy as np

def getSuperTrendTradeStrategy(
    stock_data: pd.DataFrame, 
    atr_period: int = 10, 
    multiplier: float = 3.0, 
    verbose: bool = True
):
    """
    Implementação da estratégia Supertrend para trading.
    
    Parâmetros:
    - atr_period: Período para cálculo do ATR (Average True Range)
    - multiplier: Multiplicador do ATR para definir bandas
    - verbose: Controla a exibição de logs detalhados
    """
    stock_data = stock_data.copy()
    
    # Calcular True Range
    stock_data['high'] = stock_data['high_price']
    stock_data['low'] = stock_data['low_price']
    stock_data['close'] = stock_data['close_price']
    
    # Garantir que temos dados suficientes
    if len(stock_data) < atr_period + 1:
        if verbose:
            print("⚠️ Dados insuficientes para cálculo do Supertrend. Pulando período...")
        return None
    
    # Calcular True Range (TR)
    tr1 = abs(stock_data['high'] - stock_data['low'])
    tr2 = abs(stock_data['high'] - stock_data['close'].shift())
    tr3 = abs(stock_data['low'] - stock_data['close'].shift())
    stock_data['tr'] = tr1.combine(tr2, max).combine(tr3, max)
    
    # Calcular ATR (Average True Range)
    stock_data['atr'] = stock_data['tr'].rolling(window=atr_period).mean()
    
    # Calcular as bandas básicas
    stock_data['basic_upper'] = ((stock_data['high'] + stock_data['low']) / 2) + (multiplier * stock_data['atr'])
    stock_data['basic_lower'] = ((stock_data['high'] + stock_data['low']) / 2) - (multiplier * stock_data['atr'])
    
    # Inicializar colunas
    stock_data['upper_band'] = 0.0
    stock_data['lower_band'] = 0.0
    stock_data['supertrend'] = 0.0
    stock_data['trend'] = 0
    
    # Preencher valores iniciais
    stock_data.loc[atr_period, 'upper_band'] = stock_data.loc[atr_period, 'basic_upper']
    stock_data.loc[atr_period, 'lower_band'] = stock_data.loc[atr_period, 'basic_lower']
    stock_data.loc[atr_period, 'trend'] = 1 if stock_data.loc[atr_period, 'close'] >= stock_data.loc[atr_period, 'basic_upper'] else -1
    
    # Calcular Supertrend (banda final)
    for i in range(atr_period + 1, len(stock_data)):
        curr_idx = stock_data.index[i]
        prev_idx = stock_data.index[i-1]
        
        # Banda superior
        if (stock_data.loc[curr_idx, 'basic_upper'] < stock_data.loc[prev_idx, 'upper_band'] or 
            stock_data.loc[prev_idx, 'close'] > stock_data.loc[prev_idx, 'upper_band']):
            stock_data.loc[curr_idx, 'upper_band'] = stock_data.loc[curr_idx, 'basic_upper']
        else:
            stock_data.loc[curr_idx, 'upper_band'] = stock_data.loc[prev_idx, 'upper_band']
            
        # Banda inferior
        if (stock_data.loc[curr_idx, 'basic_lower'] > stock_data.loc[prev_idx, 'lower_band'] or 
            stock_data.loc[prev_idx, 'close'] < stock_data.loc[prev_idx, 'lower_band']):
            stock_data.loc[curr_idx, 'lower_band'] = stock_data.loc[curr_idx, 'basic_lower']
        else:
            stock_data.loc[curr_idx, 'lower_band'] = stock_data.loc[prev_idx, 'lower_band']
        
        # Determinar tendência
        if stock_data.loc[prev_idx, 'trend'] == 1:
            if stock_data.loc[curr_idx, 'close'] < stock_data.loc[prev_idx, 'lower_band']:
                stock_data.loc[curr_idx, 'trend'] = -1  # Mudou para tendência de baixa
            else:
                stock_data.loc[curr_idx, 'trend'] = 1   # Manteve tendência de alta
        else:
            if stock_data.loc[curr_idx, 'close'] > stock_data.loc[prev_idx, 'upper_band']:
                stock_data.loc[curr_idx, 'trend'] = 1   # Mudou para tendência de alta
            else:
                stock_data.loc[curr_idx, 'trend'] = -1  # Manteve tendência de baixa
        
        # Determinar valor do Supertrend
        if stock_data.loc[curr_idx, 'trend'] == 1:
            stock_data.loc[curr_idx, 'supertrend'] = stock_data.loc[curr_idx, 'lower_band']
        else:
            stock_data.loc[curr_idx, 'supertrend'] = stock_data.loc[curr_idx, 'upper_band']
    
    # Verificar dados suficientes
    if len(stock_data.dropna()) < atr_period + 2:
        if verbose:
            print("⚠️ Dados insuficientes para decisão do Supertrend. Pulando período...")
        return None
    
    # Obter últimos valores para decisão
    current_trend = stock_data['trend'].iloc[-1]
    previous_trend = stock_data['trend'].iloc[-2]
    last_close = stock_data['close'].iloc[-1]
    last_supertrend = stock_data['supertrend'].iloc[-1]
    
    # Lógica de decisão para compra/venda baseada na reversão de tendência
    trade_decision = None
    if current_trend == 1 and previous_trend == -1:
        # Cruzamento para cima (sinal de compra)
        trade_decision = True
    elif current_trend == -1 and previous_trend == 1:
        # Cruzamento para baixo (sinal de venda)
        trade_decision = False
    
    # Logs detalhados
    if verbose:
        print("-------")
        print("📊 Estratégia: Supertrend")
        print(f" | Preço atual: {last_close:.6f}")
        print(f" | Valor Supertrend: {last_supertrend:.6f}")
        print(f" | Tendência atual: {'Alta' if current_trend == 1 else 'Baixa'}")
        print(f" | Tendência anterior: {'Alta' if previous_trend == 1 else 'Baixa'}")
        print(f" | ATR ({atr_period}): {stock_data['atr'].iloc[-1]:.6f}")
        print(f" | Decisão: {'Comprar' if trade_decision == True else 'Vender' if trade_decision == False else 'Nenhuma'}")
        print("-------")
    
    return trade_decision

# Criar alias para manter compatibilidade com ambas as grafias
getSupertrendTradeStrategy = getSuperTrendTradeStrategy
getSupertrendTradeStrategy = getSuperTrendTradeStrategy