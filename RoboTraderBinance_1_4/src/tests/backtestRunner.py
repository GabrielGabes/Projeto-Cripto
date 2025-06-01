import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os

# ------------------------------------------------------------------------
# 🔎 AJUSTES PADRÕES DO BACKTEST 🔎

# Parâmetros padrão do backtest
DEFAULT_PERIODS = 2000
DEFAULT_START_DATE = '2025-03-01 00:00:00'
DEFAULT_END_DATE = '2025-03-07 00:00:00'

# ------------------------------------------------------------------------
# 🧮 CONFIGURAÇÕES DE BUFFER E CÁLCULOS 🧮

# Buffer de candles para cálculo dos indicadores (ex.: média móvel de 200 períodos)
INDICATOR_BUFFER_SIZE = 300  # ~12,5 dias para candles de 60 minutos

# ------------------------------------------------------------------------
# 📊 FUNÇÃO PRINCIPAL DE BACKTEST 📊

def backtestRunner(
    stock_data: pd.DataFrame,
    strategy_function,
    nome_estrategia='',  # 🔹 Corrigido para string padrão vazia
    strategy_instance=None,
    periods=DEFAULT_PERIODS,
    initial_balance=1000,
    start_date=DEFAULT_START_DATE,
    end_date=DEFAULT_END_DATE,
    **strategy_kwargs
    ):
    print('*'*120)

    """
    Executa um backtest de uma estratégia de trading, garantindo que os indicadores 
    (ex.: média móvel de 200 períodos) sejam calculados com base em candles 
    anteriores a start_date.
    
    Mesmo estendendo o histórico, as operações serão disparadas somente 
    para os candles entre start_date e end_date.
    
    :param stock_data: DataFrame com os dados do ativo.
    :param strategy_function: Função que implementa a estratégia.
    :param strategy_instance: Instância da estratégia, se aplicável.
    :param periods: Número de períodos (usado se as datas não forem fornecidas).
    :param initial_balance: Saldo inicial.
    :param start_date: Data de início do backtest (string, datetime ou None).
    :param end_date: Data de fim do backtest (string, datetime ou None).
    :param strategy_kwargs: Parâmetros adicionais para a estratégia.
    :return: Lucro/prejuízo percentual do backtest.
    """
    # ------------------------------------------------------------------------
    # 📅 TRATAMENTO DE DATAS 📅
    
    # Se uma das datas for None, define ambas com base em periods
    if start_date is None or end_date is None:
        end_date = pd.Timestamp(datetime.now())
        start_date = end_date - pd.Timedelta(hours=periods)
    else:
        # Se as datas forem passadas como strings, converte para datetime
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        # Garante que sejam pd.Timestamp
        if not isinstance(start_date, pd.Timestamp):
            start_date = pd.Timestamp(start_date)
        if not isinstance(end_date, pd.Timestamp):
            end_date = pd.Timestamp(end_date)

    # ------------------------------------------------------------------------
    # 🔍 PREPARAÇÃO DOS DADOS 🔍
    
    # Se datas são fornecidas (ou definidas) utiliza-as; trata os diferentes formatos do DataFrame
    if isinstance(stock_data.index, pd.DatetimeIndex):
        # Ajusta o fuso das datas para o mesmo do índice, se necessário
        tz_info = stock_data.index.tz
        if tz_info is not None:
            if start_date.tzinfo is None:
                start_date = start_date.tz_localize(tz_info)
            else:
                start_date = start_date.tz_convert(tz_info)
            if end_date.tzinfo is None:
                end_date = end_date.tz_localize(tz_info)
            else:
                end_date = end_date.tz_convert(tz_info)
        stock_data = stock_data.sort_index()
        main_data = stock_data.loc[start_date:end_date].copy()
        before_data = stock_data[stock_data.index < start_date].copy().tail(INDICATOR_BUFFER_SIZE)
        full_data = pd.concat([before_data, main_data])
        extended_date = before_data.index[0] if not before_data.empty else start_date
    elif "open_time" in stock_data.columns:
        stock_data["open_time"] = pd.to_datetime(stock_data["open_time"])
        # Ajusta start_date e end_date para terem o mesmo fuso da coluna "open_time"
        tz_info = stock_data["open_time"].iloc[0].tzinfo
        if tz_info is not None:
            if start_date.tzinfo is None:
                start_date = start_date.tz_localize(tz_info)
            else:
                start_date = start_date.tz_convert(tz_info)
            if end_date.tzinfo is None:
                end_date = end_date.tz_localize(tz_info)
            else:
                end_date = end_date.tz_convert(tz_info)
        stock_data = stock_data.sort_values("open_time")
        main_data = stock_data[(stock_data["open_time"] >= start_date) & 
                               (stock_data["open_time"] <= end_date)].copy()
        before_data = stock_data[stock_data["open_time"] < start_date].copy().tail(INDICATOR_BUFFER_SIZE)
        full_data = pd.concat([before_data, main_data])
        extended_date = before_data.iloc[0]["open_time"] if not before_data.empty else start_date
    else:
        print("⚠️ Não foi possível filtrar por data. Certifique-se de que o DataFrame possui um index datetime ou a coluna 'open_time'.")
        return None

    # Impressão para verificação das datas utilizadas no cálculo dos indicadores
    print("----- Período de Cálculo dos Indicadores ---------------")
    print(f"Data inicial (start_date):           {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Data final (end_date):               {end_date.strftime('%Y-%m-%d %H:%M:%S')}")
    if isinstance(extended_date, pd.Timestamp):
        print(f"Data do primeiro candle do buffer:   {extended_date.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"Data do primeiro candle do buffer: {extended_date}")
    print("--------------------------------------------------------\n")
    
    # Deixando apenas os dados dentro do range do start_date e end_date
    full_data = full_data[(full_data['open_time'] >= start_date) & (full_data['open_time'] <= end_date)]

    # Remover linhas com NaN para evitar problemas
    full_data.dropna(inplace=True)

    # 🔹 Criando coluna formatada para eixo X (no formato desejado)
    full_data["formatted_time"] = full_data["open_time"].dt.strftime("%Y-%m-%d %H:%M")

    # Exibir o período do backtest (apenas para os candles que serão operados)
    print(f"📅 Período do Backtest: {start_date.strftime('%Y-%m-%d %H:%M:%S')} ➝  {end_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # ------------------------------------------------------------------------
    # 💰 INICIALIZAÇÃO DO BACKTEST 💰
    
    # Inicializa variáveis do backtest
    balance = initial_balance  # Saldo inicial
    position = 0  # 1 = comprado, -1 = vendido, 0 = sem posição
    entry_price = 0  # Preço de entrada na operação
    last_signal = None  # Guarda o último tipo de sinal para evitar compras/vendas consecutivas
    trades = 0  # Contador de operações

    buy_signals = []
    sell_signals = []

    # Variáveis para contar trades lucrativos e com prejuízo
    profit_trades_count = 0
    profit_trades_value = 0.0
    loss_trades_count = 0
    loss_trades_value = 0.0

    print(f"📊 Iniciando backtest da estratégia: {strategy_function.__name__}")
    print(f"🔹 Balanço inicial: ${balance:.2f}")

    # ------------------------------------------------------------------------
    # 🔄 EXECUÇÃO DO BACKTEST 🔄
    
    # Loop de execução do backtest: percorre todos os candles do conjunto estendido
    for i in range(1, len(full_data)):
        # Redefine o índice para garantir que a estratégia acesse os dados por posição
        current_data = full_data.iloc[: i+1].reset_index(drop=True)

        # Ignora candles anteriores ao start_date (ainda usados para cálculo dos indicadores)
        if "open_time" in current_data.columns:
            if current_data.iloc[-1]["open_time"] < start_date:
                continue
        else:
            pass

        # Executa a estratégia com os dados históricos até o candle atual
        if strategy_instance:
            signal = strategy_function(strategy_instance)
        else:
            signal = strategy_function(current_data, **strategy_kwargs)

        if signal is None:
            continue

        close_price = current_data.iloc[-1]["close_price"]

        # Compra apenas no primeiro sinal de compra e se não estiver comprado
        if signal and position == 0 and last_signal != "buy":
            position = 1
            entry_price = close_price
            last_signal = "buy"
            trades += 1
            buy_signals.append((full_data.iloc[i]['formatted_time'], close_price))
        # Venda apenas no primeiro sinal de venda e se estiver comprado
        elif not signal and position == 1 and last_signal != "sell":
            position = 0
            profit = ((close_price - entry_price) / entry_price) * balance
            balance += profit

            # Atualiza contagem e valores conforme o resultado da operação
            if profit > 0:
                profit_trades_count += 1
                profit_trades_value += profit
            elif profit < 0:
                loss_trades_count += 1
                loss_trades_value += profit

            last_signal = "sell"
            trades += 1
            sell_signals.append((full_data.iloc[i]['formatted_time'], close_price))

    # Caso a posição ainda esteja aberta no final, encerra a operação
    if position == 1:
        final_price = full_data.iloc[-1]["close_price"]
        profit = ((final_price - entry_price) / entry_price) * balance
        balance += profit
        if profit > 0:
            profit_trades_count += 1
            profit_trades_value += profit
        elif profit < 0:
            loss_trades_count += 1
            loss_trades_value += profit

    # ------------------------------------------------------------------------
    # 📈 RESULTADOS E MÉTRICAS 📈
    
    profit_percentage = ((balance - initial_balance) / initial_balance) * 100

    print(f"🔹 Balanço final:   ${balance:.2f}")
    print(f"📈 Lucro/prejuízo percentual: {profit_percentage:.2f}%")
    print(f"📊 Total de operações realizadas: {trades}")
    print("\n")
    print(f"✅ Operações lucrativas:   {profit_trades_count} - Valor total: ${profit_trades_value:.2f}")
    print(f"❌ Operações com prejuízo: {loss_trades_count} - Valor total: ${loss_trades_value:.2f}")
    
    # Verifica se houve lucro ou prejuízo e imprime o resultado final
    if balance > initial_balance:
        print(f"🏆 Resultado final: Lucro de ${balance - initial_balance:.2f}")
    elif balance < initial_balance:
        print(f"⚠️  Resultado final: Prejuízo de ${initial_balance - balance:.2f}")
    else:
        print("Resultado final: Sem lucro nem prejuízo.")
    
    print("\n")

    # Cálculo da Média e Percentual de Lucro e Prejuízo por Trade
    if profit_trades_count > 0:
        avg_profit_trade = profit_trades_value / profit_trades_count
    else:
        avg_profit_trade = 0

    if loss_trades_count > 0:
        avg_loss_trade = loss_trades_value / loss_trades_count  # valor negativo
    else:
        avg_loss_trade = 0

    avg_loss_trade_abs = abs(avg_loss_trade)

    avg_profit_percentage = (avg_profit_trade / initial_balance) * 100
    avg_loss_percentage = (avg_loss_trade_abs / initial_balance) * 100

    print(f"🔹 Média de Lucro por Trade   :  ${avg_profit_trade:.2f} ({avg_profit_percentage:.2f}%)")
    print(f"🔹 Média de Prejuízo por Trade:  ${avg_loss_trade_abs:.2f} ({avg_loss_percentage:.2f}%)\n")

    # ------------------------------------------------------------------------
    # --------------------- GRAFICO ---------------------
    # Criar diretório se não existir
    save_path = r"C:\Users\gabri\OneDrive\Documentos\PROJETOS PARADOS OU TERMINADOS\RoboTraderBinance_1_4\src\tests\graficos"
    os.makedirs(save_path, exist_ok=True)
    
    # Nome do arquivo baseado na estratégia
    if nome_estrategia == '':
        file_name = f"{strategy_function.__name__}.jpg"
    else:
        file_name = f"{nome_estrategia}.jpg"
    full_path = os.path.join(save_path, file_name)

    # 🔹 Criando subtítulo do gráfico
    subtitle_text = f"Balanço Final: ${balance:.2f} | Lucro/Prejuízo: {profit_percentage:.2f}% | Operações: {trades}"

    # Plotando os resultados
    plt.figure(figsize=(21.6, 10.8), dpi=100)  # 🔹 Ajustado para tela cheia

    # plt.plot(full_data["close_price"], label="Preço de Fechamento", color="blue")
    plt.plot(full_data["formatted_time"], full_data["close_price"], label="Preço de Fechamento", color="blue")

    if buy_signals:
        # buy_indices, buy_prices = zip(*buy_signals)
        buy_indices, buy_prices = zip(*buy_signals) if buy_signals else ([], [])
        plt.scatter(buy_indices, buy_prices, marker="^", color="green", label="Compra", s=100, edgecolors='black')
    if sell_signals:
        # sell_indices, sell_prices = zip(*sell_signals)
        sell_indices, sell_prices = zip(*sell_signals) if sell_signals else ([], [])
        plt.scatter(sell_indices, sell_prices, marker="v", color="red", label="Venda", s=100, edgecolors='black')

    plt.xlabel("Data e Hora")
    plt.ylabel("Preço")
    plt.legend()
    
    # 🔹 Corrigido título do gráfico
    plt.title(f"Estratégia de Trading: {nome_estrategia} ({strategy_function.__name__})\n{subtitle_text}")

    qtde_valores_mostrar_eixo_x = 40
    plt.xticks(ticks=np.linspace(0, len(full_data) - 1, num=qtde_valores_mostrar_eixo_x, dtype=int), 
               labels=full_data['formatted_time'].iloc[np.linspace(0, len(full_data) - 1, num=qtde_valores_mostrar_eixo_x, dtype=int)], 
               rotation=90)
    plt.grid()

    # Salvar o gráfico no caminho especificado
    plt.savefig(full_path, format='jpg', dpi=300, bbox_inches='tight')

    # Exibir gráfico na tela
    # plt.show()  # Comentado caso não queira exibir sempre

    print(f"📊 Gráfico salvo em: {full_path}")

    print('*'*120)

    return profit_percentage