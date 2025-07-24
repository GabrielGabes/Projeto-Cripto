import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os
import pytz
import traceback ## Obter todas informações sobre o erro
import time

# ------------------------------------------------------------------------
# 📊 FUNÇÃO PRINCIPAL DE BACKTEST 📊

def backtestRunner(
        stock_data: pd.DataFrame,
        strategy_function,
        nome_estrategia='',  # 🔹 Corrigido para string padrão vazia
        strategy_instance=None,
        initial_balance=1000,
        start_date='',
        end_date='',
        **strategy_kwargs
    ):
    try:
        print('*'*120)

        inicio = time.time()

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

        full_data = stock_data.copy()
        # 🔹 Criando coluna formatada para eixo X (no formato desejado)
        full_data["formatted_time"] = full_data["open_time"].dt.strftime("%Y-%m-%d %H:%M")
        # ------------------------------------------------------------------------
        # 📅 TRATAMENTO DE DATAS 📅

        tz = pytz.timezone("America/Sao_Paulo")
        start_date = tz.localize(datetime.strptime(start_date, "%d/%m/%Y %H:%M"))
        end_date = tz.localize(datetime.strptime(end_date, "%d/%m/%Y %H:%M"))
        
        # Impressão para verificação das datas utilizadas no cálculo dos indicadores
        print("----- Período de Cálculo dos Indicadores ---------------")
        print(f"Data inicial (start_date):           {full_data['open_time'].min()}")
        print(f"Data final (end_date):               {full_data['open_time'].max()}")
        print("--------------------------------------------------------\n")
        
        # ⚠️ Mantém os dados com buffer completo
        extended_data = full_data.copy()

        # 🔹 Filtra apenas os dados do intervalo de operação para aplicar a estratégia 
        # Deixando apenas os dados dentro do range do start_date e end_date
        backtest_data = extended_data[(extended_data['open_time'] >= start_date) & (extended_data['open_time'] <= end_date)]

        # Remover linhas com NaN para evitar problemas
        extended_data.dropna(inplace=True)

        # print('\n', extended_data['open_time'].describe())

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
        profit_trades_value = 0
        loss_trades_count = 0
        loss_trades_value = 0

        print(f"📊 Iniciando backtest da estratégia: {strategy_function.__name__}")
        print(f"🔹 Balanço inicial: ${balance:.2f}")

        # ------------------------------------------------------------------------
        # 🔄 EXECUÇÃO DO BACKTEST 🔄
        count = 0
        extended_data['signal'] = np.nan
        extended_data['acao_tomada'] = np.nan
        # Loop de execução do backtest: percorre todos os candles do conjunto estendido
        for i in range(0, len(extended_data)+1):

            # Redefine o índice para garantir que a estratégia acesse os dados por posição
            current_data = extended_data.iloc[: i+1].reset_index(drop=True)

            # Ignora candles anteriores ao start_date (ainda usados para cálculo dos indicadores)
            if current_data.iloc[-1]["open_time"] < start_date:
                continue
            
            # if count == 0:
            #     print(extended_data.iloc[i])
            # count += 1

            # Executa a estratégia com os dados históricos até o candle atual
            if strategy_instance:
                signal = strategy_function(strategy_instance, all_metrics_return = True)
            else:
                signal = strategy_function(current_data, all_metrics_return = True, **strategy_kwargs)

            # Extraindo as metricas da estrategias
            strategy_metrics = signal[1] # DATAFRAME COM METRICAS DA ESTRATEGIA
            signal = signal[0] # SINAL DE COMPRA OU VENDA
            extended_data.loc[i, 'signal'] = signal

            for coluna in strategy_metrics.columns: # ACRESCENTANDO AS METRICAS DA ESTRATEGIA NO DATAFRAME COM PRECOS
                if coluna not in extended_data.columns:
                    extended_data[coluna] = np.nan
                extended_data.loc[i, coluna] = strategy_metrics[coluna].iloc[-1]

            if signal is None:
                continue

            close_price = current_data.iloc[-1]["close_price"]

            # Compra apenas no primeiro sinal de compra e se não estiver comprado
            if signal and position == 0 and last_signal != "buy":
                position = 1
                entry_price = close_price
                last_signal = "buy"
                extended_data.loc[i, 'acao_tomada'] = last_signal # registrando compra
                trades += 1
                buy_signals.append((extended_data.iloc[i]['formatted_time'], close_price))

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
                extended_data.loc[i, 'acao_tomada'] = last_signal # registrando venda
                trades += 1
                sell_signals.append((extended_data.iloc[i]['formatted_time'], close_price))

        # Caso a posição ainda esteja aberta no final, encerra a operação
        if position == 1:
            final_price = extended_data.iloc[-1]["close_price"]
            profit = ((final_price - entry_price) / entry_price) * balance
            balance += profit
            if profit > 0:
                profit_trades_count += 1
                profit_trades_value += profit
            elif profit < 0:
                loss_trades_count += 1
                loss_trades_value += profit

        # print(extended_data['acao_tomada'].value_counts(), '\n')
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

        fim = time.time()
        tempo_cronometrado = fim - inicio
        print('Tempo para rodar simulação (s):', tempo_cronometrado)
        # ------------------------------------------------------------------------
        # --------------------- GRAFICO ---------------------
        # Criar diretório se não existir
        # save_path = r"C:\Users\gabri\OneDrive\Documentos\Criptos\RoboTraderBinance_1_4b\src\tests\graficos"
        # os.makedirs(save_path, exist_ok=True)
        
        # # Nome do arquivo baseado na estratégia
        # if nome_estrategia == '':
        #     file_name = f"{strategy_function.__name__}.jpg"
        # else:
        #     file_name = f"{nome_estrategia}.jpg"
        # full_path = os.path.join(save_path, file_name)

        # # 🔹 Criando subtítulo do gráfico
        # subtitle_text = f"Balanço Final: ${balance:.2f} | Lucro/Prejuízo: {profit_percentage:.2f}% | Operações: {trades}"

        # # Plotando os resultados
        # plt.figure(figsize=(21.6, 10.8), dpi=100)  # 🔹 Ajustado para tela cheia

        # # plt.plot(backtest_data["close_price"], label="Preço de Fechamento", color="blue")
        # plt.plot(backtest_data["formatted_time"], backtest_data["close_price"], label="Preço de Fechamento", color="blue")

        # if buy_signals:
        #     # buy_indices, buy_prices = zip(*buy_signals)
        #     buy_indices, buy_prices = zip(*buy_signals) if buy_signals else ([], [])
        #     plt.scatter(buy_indices, buy_prices, marker="^", color="green", label="Compra", s=100, edgecolors='black')
        # if sell_signals:
        #     # sell_indices, sell_prices = zip(*sell_signals)
        #     sell_indices, sell_prices = zip(*sell_signals) if sell_signals else ([], [])
        #     plt.scatter(sell_indices, sell_prices, marker="v", color="red", label="Venda", s=100, edgecolors='black')

        # plt.xlabel("Data e Hora")
        # plt.ylabel("Preço")
        # plt.legend()
        
        # # 🔹 Corrigido título do gráfico
        # plt.title(f"Estratégia de Trading: {nome_estrategia} ({strategy_function.__name__})\n{subtitle_text}")

        # qtde_valores_mostrar_eixo_x = min(40, len(extended_data))
        # plt.xticks(ticks=np.linspace(0, len(extended_data) - 1, num=qtde_valores_mostrar_eixo_x, dtype=int), 
        #            labels=extended_data['formatted_time'].iloc[np.linspace(0, len(extended_data) - 1, num=qtde_valores_mostrar_eixo_x, dtype=int)], 
        #            rotation=90)
        # plt.grid()

        # # Salvar o gráfico no caminho especificado
        # plt.savefig(full_path, format='jpg', dpi=300, bbox_inches='tight')

        # # Exibir gráfico na tela
        # # plt.show()  # Comentado caso não queira exibir sempre

        # print(f"📊 Gráfico salvo em: {full_path}")

        # ------------------------------------------------------------------------
        # print(extended_data[extended_data['acao_tomada'].notnull()])
        return [
            nome_estrategia if nome_estrategia != '' else strategy_function.__name__,  # Nome da estratégia
            start_date,
            end_date,
            balance,
            profit_percentage,
            trades,
            profit_trades_count,
            profit_trades_value,
            loss_trades_count,
            loss_trades_value,
            avg_profit_trade,
            avg_profit_percentage,
            avg_loss_trade_abs,
            avg_loss_percentage,
            tempo_cronometrado
        ], current_data
    except Exception as e:
        print(traceback.format_exc())
        return [
            nome_estrategia if nome_estrategia != '' else strategy_function.__name__,  # Nome da estratégia
            start_date,
            end_date,
            balance,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan
        ], current_data


#| Índice | Métrica                 | Descrição                                          |
#| ------ | ----------------------- | -------------------------------------------------- |
#| 0      | `nome_estrategia`       | Nome da estratégia usada                           |
#| 1      | `start_date`            | Data inicial do backtest                           |
#| 2      | `end_date`              | Data final do backtest                             |
#| 3      | `balance`               | Saldo final em dólar                               |
#| 4      | `profit_percentage`     | Lucro/prejuízo percentual                          |
#| 5      | `trades`                | Total de operações (buy + sell)                    |
#| 6      | `profit_trades_count`   | Nº de trades lucrativos                            |
#| 7      | `profit_trades_value`   | Valor somado dos trades com lucro                  |
#| 8      | `loss_trades_count`     | Nº de trades com prejuízo                          |
#| 9      | `loss_trades_value`     | Valor somado dos trades com prejuízo               |
#| 10     | `avg_profit_trade`      | Lucro médio por trade positivo                     |
#| 11     | `avg_profit_percentage` | Percentual médio de lucro por trade positivo       |
#| 12     | `avg_loss_trade_abs`    | Prejuízo médio por trade negativo (valor absoluto) |
#| 13     | `avg_loss_percentage`   | Percentual médio de prejuízo por trade negativo    |