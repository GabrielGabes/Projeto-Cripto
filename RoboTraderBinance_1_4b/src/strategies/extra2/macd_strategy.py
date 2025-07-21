import pandas as pd
import numpy as np

def getMACDTradeStrategy(
    stock_data: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    verbose: bool = True,
    all_metrics_return: bool = True
):
    """
    Estratégia MACD (Moving Average Convergence Divergence) para negociação.
    
    - Compra quando a linha MACD cruza acima da linha de sinal
    - Venda quando a linha MACD cruza abaixo da linha de sinal
    
    Parâmetros:
    - fast_period: Período para a média móvel rápida
    - slow_period: Período para a média móvel lenta
    - signal_period: Período para a linha de sinal (média móvel do MACD)
    """
    stock_data = stock_data.copy()
    
    # Calcular MACD
    fast_ema = stock_data['close_price'].ewm(span=fast_period, min_periods=fast_period).mean()
    slow_ema = stock_data['close_price'].ewm(span=slow_period, min_periods=slow_period).mean()
    
    # MACD Line = Fast EMA - Slow EMA
    stock_data['macd'] = fast_ema - slow_ema
    
    # Signal Line = EMA of MACD Line
    stock_data['macd_signal'] = stock_data['macd'].ewm(span=signal_period, min_periods=signal_period).mean()
    
    # MACD Histogram = MACD Line - Signal Line
    stock_data['macd_hist'] = stock_data['macd'] - stock_data['macd_signal']
    
    # Remover NaN
    stock_data.dropna(subset=['macd', 'macd_signal'], inplace=True)
    
    # Verificar se temos dados suficientes
    if len(stock_data) < max(fast_period, slow_period, signal_period):
        if verbose:
            print("⚠️ Dados insuficientes para cálculo do MACD. Pulando período...")
        return None
    
    # Últimos valores do MACD
    last_macd = stock_data['macd'].iloc[-1]
    last_signal = stock_data['macd_signal'].iloc[-1]
    last_hist = stock_data['macd_hist'].iloc[-1]
    prev_hist = stock_data['macd_hist'].iloc[-2]
    
    # Decisão de compra/venda
    buy_condition = prev_hist < 0 and last_hist > 0  # Cruzamento positivo do histograma
    sell_condition = prev_hist > 0 and last_hist < 0  # Cruzamento negativo do histograma
    
    trade_decision = True if buy_condition else False if sell_condition else None
    
    if verbose:
        print("-------")
        print("📊 Estratégia: MACD")
        print(f" | Linha MACD: {last_macd:.6f}")
        print(f" | Linha de Sinal: {last_signal:.6f}")
        print(f" | Histograma MACD: {last_hist:.6f}")
        print(f" | Decisão: {'Comprar' if trade_decision == True else 'Vender' if trade_decision == False else 'Nenhuma'}")
        print("-------")
    
    if all_metrics_return == True:
        metrics = {
            # 'close_price':stock_data['close_price'],
            'open_time_join':stock_data['open_time'],
            # 'open_price':stock_data['open_price'],
            # 'high_price':stock_data['high_price'],
            # 'low_price':stock_data['low_price'],
            # 'volume':stock_data['volume'],
            'last_macd': stock_data['macd'],
            'last_signal': stock_data['macd_signal'],
            'macd_hist': stock_data['macd_hist']
        }
        metrics = pd.DataFrame(metrics)
        return trade_decision, metrics
    else:
        return trade_decision