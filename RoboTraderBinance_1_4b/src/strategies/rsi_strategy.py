import pandas as pd
from indicators import Indicators


def getRsiTradeStrategy(stock_data: pd.DataFrame, low=30, high=70, verbose=True, all_metrics_return = True):

    stock_data = stock_data.copy()  # Importante para evitar bugs

    # **Calcula o RSI e adiciona ao DataFrame**
    stock_data["RSI"] = Indicators.getRSI(stock_data["close_price"], last_only=False)

    if "RSI" not in stock_data.columns:
        raise ValueError("O DataFrame deve conter a coluna 'RSI'. Verifique se o RSI foi calculado.")

    rsi_series = stock_data["RSI"]
    last_rsi = rsi_series.iloc[-1]  # Último valor do RSI

    # Identifica os momentos em que RSI cruzou os níveis de sobrecompra e sobrevenda
    peaks = stock_data[rsi_series > high].index
    valleys = stock_data[rsi_series < low].index

    # Encontra o último pico e o último vale
    last_peak = peaks[-1] if len(peaks) > 0 else None
    last_valley = valleys[-1] if len(valleys) > 0 else None

    trade_decision = None  # Mantém a posição até uma nova condição

    if last_valley and (last_peak is None or last_valley > last_peak):
        # Último evento foi um vale (RSI < 30), mas ainda não passou de 70 → Mantém compra
        trade_decision = True

    elif last_peak and (last_valley is None or last_peak > last_valley):
        # Último evento foi um pico (RSI > 70), mas ainda não caiu até 30 → Mantém venda
        trade_decision = False

    if verbose:
        print("-------")
        print("📊 Estratégia: RSI - Vales e Topos")
        print(f" | Último RSI: {last_rsi}")
        print(f" | Último Vale: {last_valley}")
        print(f" | Último Pico: {last_peak}")
        print(f' | Decisão: {"Comprar" if trade_decision == True else "Vender" if trade_decision == False else "Nenhuma"}')

        print("-------")
    
    if all_metrics_return == True:
        metrics = {
            # 'close_price':stock_data['close_price'],
            'open_time_join': stock_data['open_time'],
            # 'open_price':stock_data['open_price'],
            # 'high_price':stock_data['high_price'],
            # 'low_price':stock_data['low_price'],
            # 'volume':stock_data['volume'],
            'RSI': stock_data["RSI"]
        }
        metrics = pd.DataFrame(metrics)
        return trade_decision, metrics
    else:
        return trade_decision