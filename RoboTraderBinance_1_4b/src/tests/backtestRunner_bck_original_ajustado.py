import numpy as np
import pandas as pd
import pytz
from datetime import datetime

# ------------------------------------------------------------------------
# 🔎 AJUSTES PADRÕES DO BACKTEST 🔎
DEFAULT_START_DATE = '2025-03-01 00:00:00'
DEFAULT_END_DATE = '2025-03-07 00:00:00'
INDICATOR_BUFFER_SIZE = 300

# ------------------------------------------------------------------------
# 📊 FUNÇÃO PRINCIPAL DE BACKTEST 📊

def backtestRunner(
    stock_data: pd.DataFrame, 
    strategy_function, 
    strategy_instance=None, 
    initial_balance=1000, 
    start_date='',
    end_date='',
    **strategy_kwargs
):
    print("----- Período de Cálculo dos Indicadores ---------------")
    tz = pytz.timezone("America/Sao_Paulo")
    start_date = tz.localize(datetime.strptime(start_date, "%d/%m/%Y %H:%M"))
    end_date = tz.localize(datetime.strptime(end_date, "%d/%m/%Y %H:%M"))
    
    print(f"Data inicial (start_date):           {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data final (end_date):               {end_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # 🔄 Filtra os dados necessários (antes e depois de start_date)
    stock_data = stock_data.sort_values("open_time")
    main_data = stock_data[(stock_data["open_time"] >= start_date) & (stock_data["open_time"] <= end_date)].copy()
    before_data = stock_data[stock_data["open_time"] < start_date].copy().tail(INDICATOR_BUFFER_SIZE)
    full_data = pd.concat([before_data, main_data]).reset_index(drop=True)

    # 🔧 Remove NaNs iniciais
    full_data.dropna(inplace=True)

    # Inicializa variáveis do backtest
    balance = initial_balance  # Saldo inicial
    position = 0  # 1 = comprado, -1 = vendido, 0 = sem posição
    entry_price = 0  # Preço de entrada na operação
    last_signal = None  # Guarda o último tipo de sinal para evitar compras/vendas consecutivas
    trades = 0  # Contador de operações

    print(f"📊 Iniciando backtest da estratégia: {strategy_function.__name__}")
    print(f"🔹 Balanço inicial: ${balance:.2f}")

    # 🔄 Loop de execução
    for i in range(1, len(full_data)):
        current_time = full_data.iloc[i]["open_time"]

        # Ignora candles antes do start_date (úteis só para indicadores)
        if current_time < start_date:
            continue

        current_data = full_data.iloc[: i + 1].copy()

        
        if strategy_instance:
            signal = strategy_function(strategy_instance)
        else:
            signal = strategy_function(current_data, **strategy_kwargs)
        if signal is None:
            continue

        close_price = full_data.iloc[i]["close_price"]

        if signal and position == 0 and last_signal != "buy":
            position = 1
            entry_price = close_price
            last_signal = "buy"
            trades += 1

        elif not signal and position == 1 and last_signal != "sell":
            position = 0
            profit = ((close_price - entry_price) / entry_price) * balance
            balance += profit
            last_signal = "sell"
            trades += 1

    # Fecha posição aberta no final
    if position == 1:
        final_price = full_data.iloc[-1]["close_price"]
        profit = ((final_price - entry_price) / entry_price) * balance
        balance += profit

    profit_percentage = ((balance - initial_balance) / initial_balance) * 100

    print(f"🔹 Balanço final: ${balance:.2f}")
    print(f"📈 Lucro/prejuízo percentual: {profit_percentage:.2f}%")
    print(f"📊 Total de operações realizadas: {trades}")

    return profit_percentage