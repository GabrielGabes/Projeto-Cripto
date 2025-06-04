import pandas as pd
import numpy as np


def getMovingAverageRSIVolumeStrategy(
    stock_data: pd.DataFrame,
    fast_window: int = 7,
    medium_window: int = 22,  
    slow_window: int = 40,
    rsi_window: int = 14,
    rsi_overbought: int = 70,
    rsi_oversold: int = 30,
    volume_multiplier: float = 1.5,
    use_atr: bool = False,
    atr_period: int = 14,
    atr_multiplier: float = 2.0,
    verbose: bool = True,
):
    """
    Estratégia Avançada de Médias Móveis com confirmação de RSI e Volume/ATR.

    - Compra quando a média rápida cruza acima da média média e a média média cruza acima da média lenta, 
      RSI está acima da zona de sobrevenda e o volume está acima da média.
    - Venda quando a média rápida cruza abaixo da média média ou RSI está na zona de sobrecompra.
    - Opcional: Usa ATR para calcular trailing stop
    
    Parâmetros:
    - fast_window: Período da média móvel rápida
    - medium_window: Período da média móvel média
    - slow_window: Período da média móvel lenta
    - rsi_window: Período para cálculo do RSI
    - rsi_overbought: Nível de sobrecompra do RSI
    - rsi_oversold: Nível de sobrevenda do RSI
    - volume_multiplier: Multiplicador para considerar volume acima da média
    - use_atr: Usar ATR para stop loss (True/False)
    - atr_period: Período para cálculo do ATR
    - atr_multiplier: Multiplicador do ATR para trailing stop
    """
    stock_data = stock_data.copy()

    # Calcula as Médias Móveis
    stock_data["ma_fast"] = stock_data["close_price"].rolling(window=fast_window).mean()
    stock_data["ma_medium"] = stock_data["close_price"].rolling(window=medium_window).mean()
    stock_data["ma_slow"] = stock_data["close_price"].rolling(window=slow_window).mean()

    # Calcula o RSI
    delta = stock_data["close_price"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
    rs = gain / loss
    stock_data["rsi"] = 100 - (100 / (1 + rs))

    # Calcula a Média do Volume
    stock_data["volume_avg"] = stock_data["volume"].rolling(window=slow_window).mean()
    
    # Calcula ATR se ativado
    if use_atr:
        high_low = stock_data['high_price'] - stock_data['low_price']
        high_close = np.abs(stock_data['high_price'] - stock_data['close_price'].shift())
        low_close = np.abs(stock_data['low_price'] - stock_data['close_price'].shift())
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        stock_data['atr'] = true_range.rolling(window=atr_period).mean()
        
        # Calcula trailing stop
        stock_data['trailing_stop'] = stock_data['close_price'] - (stock_data['atr'] * atr_multiplier)
        
        # Adiciona aos subsets para remover NaN
        drop_subset = ["ma_fast", "ma_medium", "ma_slow", "rsi", "volume_avg", "atr", "trailing_stop"]
    else:
        drop_subset = ["ma_fast", "ma_medium", "ma_slow", "rsi", "volume_avg"]

    # Remove NaN
    stock_data.dropna(subset=drop_subset, inplace=True)
    
    # Verificar período mínimo de dados
    min_period = max(slow_window, rsi_window)
    if use_atr:
        min_period = max(min_period, atr_period)
        
    if len(stock_data) < min_period:
        if verbose:
            print("⚠️ Dados insuficientes após remoção de NaN. Pulando período...")
        return None

    # Últimos valores dos indicadores
    last_ma_fast = stock_data["ma_fast"].iloc[-1]
    last_ma_medium = stock_data["ma_medium"].iloc[-1]
    last_ma_slow = stock_data["ma_slow"].iloc[-1]
    last_rsi = stock_data["rsi"].iloc[-1]
    last_volume = stock_data["volume"].iloc[-1]
    last_volume_avg = stock_data["volume_avg"].iloc[-1]
    last_close = stock_data["close_price"].iloc[-1]
    
    # ATR e trailing stop (se ativados)
    last_trailing_stop = None
    if use_atr:
        last_atr = stock_data["atr"].iloc[-1]
        last_trailing_stop = stock_data["trailing_stop"].iloc[-1]

    # Condições para compra
    volume_condition = last_volume > (volume_multiplier * last_volume_avg)
    ma_condition = (last_ma_fast > last_ma_medium) and (last_ma_medium > last_ma_slow)
    rsi_buy_condition = last_rsi > rsi_oversold
    
    buy_condition = ma_condition and rsi_buy_condition and volume_condition

    # Condições para venda
    ma_sell_condition = last_ma_fast < last_ma_medium
    rsi_sell_condition = last_rsi > rsi_overbought
    
    # Adiciona trailing stop à condição de venda se ATR estiver ativado
    trailing_stop_condition = False
    if use_atr and last_trailing_stop is not None:
        trailing_stop_condition = last_close < last_trailing_stop
    
    sell_condition = ma_sell_condition or rsi_sell_condition or trailing_stop_condition

    trade_decision = True if buy_condition else False if sell_condition else None

    if verbose:
        print("-------")
        print("📊 Estratégia: Médias Móveis + RSI + Volume" + (" + ATR" if use_atr else ""))
        print(f" | Última Média Rápida (MA{fast_window}): {last_ma_fast:.3f}")
        print(f" | Última Média Média (MA{medium_window}): {last_ma_medium:.3f}")
        print(f" | Última Média Lenta (MA{slow_window}): {last_ma_slow:.3f}")
        print(f" | Último Preço: {last_close:.3f}")
        print(f" | Último RSI: {last_rsi:.3f}")
        print(f" | Último Volume: {last_volume:.3f}")
        print(f" | Média de Volume: {last_volume_avg:.3f}")
        
        if use_atr and last_trailing_stop is not None:
            print(f" | ATR: {last_atr:.3f}")
            print(f" | Trailing Stop: {last_trailing_stop:.3f}")
            
        print(f' | Decisão: {"Comprar" if trade_decision == True else "Vender" if trade_decision == False else "Nenhuma"}')
        print("-------")

    return trade_decision