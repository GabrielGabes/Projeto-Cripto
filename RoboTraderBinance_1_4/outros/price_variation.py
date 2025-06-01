import ccxt
import pandas as pd
import numpy as np
import time
from tabulate import tabulate

def build_variation_table():
    def get_usdt_pairs():
        """Obtém todos os pares USDT ativos no Spot."""
        binance = ccxt.binance()
        markets = binance.load_markets()
        return [symbol for symbol, details in markets.items() if symbol.endswith('/USDT') and details.get('active', False) and details.get('spot', True)]

    binance = ccxt.binance()
    usdt_pairs = get_usdt_pairs()
    results = []

    for symbol in usdt_pairs:
        try:
            ticker = binance.fetch_ticker(symbol)
            var_24h = ticker.get('percentage', None)  # variação de 24h fornecida pela Binance

            if var_24h is None:
                continue

            ohlcv = binance.fetch_ohlcv(symbol, timeframe='1h', limit=2)
            if len(ohlcv) < 2:
                continue

            price_1h_ago = ohlcv[-2][4]
            current_price = ticker['last']
            var_1h = ((current_price - price_1h_ago) / price_1h_ago) * 100

            results.append({
                'Ativo': symbol,
                'Variação_1h_%': round(var_1h, 2),
                'Variação_24h_%': round(var_24h, 2)
            })

            time.sleep(0.2)

        except Exception as e:
            print(f"Erro ao processar {symbol}: {e}")
            continue

    df = pd.DataFrame(results)
    if df.empty:
        print("Nenhum ativo processado com sucesso.")
        return df

    df['Classificação'] = np.nan

    # Classificação: Saída de Lateralidade
    cond1 = df['Variação_1h_%'] >= 1
    cond2 = (df['Variação_24h_%'] < 1) & (df['Variação_24h_%'] > -1)
    df.loc[cond1 & cond2, 'Classificação'] = 'Saída de Lateralidade'

    # Classificação: Fortes líderes de tendência (momentum play)
    cond3 = df['Variação_1h_%'] >= 1
    cond4 = df['Variação_24h_%'] >= 5
    df.loc[cond3 & cond4, 'Classificação'] = 'Momentum Play'

    # Classificação: Reversão (pullback)
    cond5 = df['Variação_1h_%'] >= 1
    cond6 = df['Variação_24h_%'] <= -5
    df.loc[cond5 & cond6, 'Classificação'] = 'Reversão / Pullback'

    df = df.sort_values(by='Variação_24h_%', ascending=False).reset_index(drop=True)
    # df.to_csv('variacao_percentual_classificada_binance.csv', index=False)

    texto_final = "\nResumo das classificações encontradas:\n"
    resumo = df['Classificação'].value_counts()
    texto_final += tabulate(resumo.to_frame(name='Quantidade'), headers='keys', tablefmt='pretty') + "\n"

    if 'Saída de Lateralidade' in resumo.index:
        texto_final += "\nMoedas em 'Saída de Lateralidade':\n"
        texto_final += tabulate(df[df['Classificação'] == 'Saída de Lateralidade'][['Ativo', 'Variação_1h_%', 'Variação_24h_%']], headers='keys', tablefmt='pretty') + "\n"

    if 'Momentum Play' in resumo.index:
        texto_final += "\nMoedas classificadas como 'Momentum Play':\n"
        texto_final += tabulate(df[df['Classificação'] == 'Momentum Play'][['Ativo', 'Variação_1h_%', 'Variação_24h_%']], headers='keys', tablefmt='pretty') + "\n"

    if 'Reversão / Pullback' in resumo.index:
        texto_final += "\nMoedas classificadas como 'Reversão / Pullback':\n"
        texto_final += tabulate(df[df['Classificação'] == 'Reversão / Pullback'][['Ativo', 'Variação_1h_%', 'Variação_24h_%']], headers='keys', tablefmt='pretty') + "\n"

    # print(texto_final)
    return texto_final

# build_variation_table()

