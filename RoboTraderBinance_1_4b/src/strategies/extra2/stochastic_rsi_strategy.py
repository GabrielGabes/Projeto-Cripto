import pandas as pd
from indicators import Indicators

def getStochasticRsiStrategy(stock_data, rsi_period=14, stoch_period=14, k_period=3, d_period=3, verbose=True, all_metrics_return=True):
    """
    Estratégia baseada no Stochastic RSI.
    
    Args:
        stock_data: DataFrame com dados de preço
        rsi_period: Período para cálculo do RSI
        stoch_period: Período para cálculo do Stochastic
        k_period: Período para a linha %K do Stochastic
        d_period: Período para a linha %D do Stochastic
        verbose: Se True, imprime informações detalhadas
    """
    stock_data = stock_data.copy()
    
    # Calcular o Stochastic RSI
    k_line, d_line = Indicators.getStochasticRSI(
        stock_data["close_price"], 
        rsi_period=rsi_period, 
        stoch_period=stoch_period, 
        k_period=k_period, 
        d_period=d_period
    )
    
    # Obter os últimos valores
    last_k = k_line.iloc[-1] if isinstance(k_line, pd.Series) else k_line
    last_d = d_line.iloc[-1] if isinstance(d_line, pd.Series) else d_line
    
    if verbose:
        print("-------")
        print("📊 Estratégia: Stochastic RSI")
        print(f" | Período RSI: {rsi_period}")
        print(f" | Período Stochastic: {stoch_period}")
        print(f" | Linha %K: {last_k:.2f}")
        print(f" | Linha %D: {last_d:.2f}")
        
    trade_decision = None
    
    if last_k > 80 and last_d > 80 and last_k < last_d:
        if verbose:
            print(" | Decisão: Vender (sobrecomprado)")
        trade_decision = False
    elif last_k < 20 and last_d < 20 and last_k > last_d:
        if verbose:
            print(" | Decisão: Comprar (sobrevendido)")
        trade_decision = True
    else:
        if verbose:
            print(" | Decisão: Nenhuma")
        trade_decision = None

    if all_metrics_return == True:
        metrics = {
            'open_time_join': stock_data['open_time'],
            'stoch_rsi_k': k_line,
            'stoch_rsi_d': d_line,
        }
        metrics = pd.DataFrame(metrics)
        return trade_decision, metrics
    else:
        return trade_decision