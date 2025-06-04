import pandas as pd
import numpy as np
from indicators.vortex import vortex  # Importa a função vortex do arquivo vortex.py

# ------------------------------------------------------------------------
# 🔎 PARÂMETROS DOS INDICADORES 🔎

# Parâmetros padrão para Médias Móveis
DEFAULT_M7_PERIOD = 7
DEFAULT_M50_PERIOD = 50
DEFAULT_M200_PERIOD = 200

# Parâmetros padrão para RSI
DEFAULT_RSI_PERIOD = 14

# Parâmetros padrão para Estocástico
DEFAULT_SLOWK_WINDOW = 2
DEFAULT_SLOW_STOCHASTIC_SMOOTHING_WINDOW = 3

# Parâmetros padrão para Vortex
DEFAULT_VORTEX_WINDOW = 14

# ------------------------------------------------------------------------
# 🧮 FUNÇÕES AUXILIARES DE CÁLCULO 🧮

def compute_RSI(series: pd.Series, period: int) -> pd.Series:
    """
    Calcula o RSI utilizando o método de Wilder (média exponencial) para suavização,
    com um período padrão de 14.
    """
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    
    # Cálculo da média exponencial com alpha = 1/period, conforme o método de Wilder
    avg_gain = up.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = down.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ------------------------------------------------------------------------
# 📊 ESTRATÉGIA AVANÇADA (VORTEX + OUTROS) 📊

def getAdvancedTradeStrategy(
    stock_data: pd.DataFrame,
    m7_period: int = DEFAULT_M7_PERIOD,
    m200_period: int = DEFAULT_M200_PERIOD,
    m50_period: int = DEFAULT_M50_PERIOD,
    rsi_period: int = DEFAULT_RSI_PERIOD,
    slowK_window: int = DEFAULT_SLOWK_WINDOW,
    slow_stochastic_smoothing_window: int = DEFAULT_SLOW_STOCHASTIC_SMOOTHING_WINDOW,
    vortex_window: int = DEFAULT_VORTEX_WINDOW,
    verbose: bool = True
):
    """
    Estratégia avançada para criptomoedas, utilizando a função 'vortex'
    importada do arquivo vortex.py para calcular o Indicador Vortex.
    
    Cada indicador é calculado com o período correspondente:
      - M7: média móvel de 'm7_period' períodos.
      - M200: média móvel de 'm200_period' períodos.
      - M50: média móvel de 'm50_period' períodos.
      - RSI: período de 'rsi_period'.
      - Slow Stochastic: %K calculado com 'slowK_window' períodos e suavização com 'slow_stochastic_smoothing_window'.
      - Vortex: calculado com 'vortex_window' períodos.
    
    Condições para COMPRA:
      1. VIP (VI+) > VIM (VI-) no período atual
      2. VIP (VI+) < VIM (VI-) no período anterior
      
    Condições para VENDA:
      a. Se VIP < VIM no período atual
      b. Se o Slow Stochastic do período anterior (Sst[1]) > 65

    Retorna True para sinal de compra e False para sinal de venda.
    """
    # ------------------------------------------------------------------------
    # 🔍 PREPARAÇÃO DOS DADOS 🔍
    
    df = stock_data.copy()
    df.sort_values("open_time", inplace=True)

    # ------------------------------------------------------------------------
    # 📊 CÁLCULO DOS INDICADORES 📊
    
    # Cálculo das Médias Móveis utilizando min_periods=1
    df["M7"]   = df["close_price"].rolling(window=m7_period, min_periods=1).mean()
    df["M200"] = df["close_price"].rolling(window=m200_period, min_periods=1).mean()
    df["M50"]  = df["close_price"].rolling(window=m50_period, min_periods=1).mean()
    
    # Cálculo do RSI
    df["RSI14"] = compute_RSI(df["close_price"], rsi_period)
    
    # Cálculo do Slow Stochastic utilizando min_periods=1
    df["lowest_low"]   = df["low_price"].rolling(window=slowK_window, min_periods=slowK_window).min()
    df["highest_high"] = df["high_price"].rolling(window=slowK_window, min_periods=slowK_window).max()
    df["fast_K"] = 100 * (df["close_price"] - df["lowest_low"]) / (df["highest_high"] - df["lowest_low"])
    df["SlowS"] = df["fast_K"].rolling(window=slow_stochastic_smoothing_window, min_periods=slow_stochastic_smoothing_window).mean()

    # Cálculo do Indicador Vortex utilizando a função importada e preenchendo os NaN com backfill.
    df["VIP"] = vortex(df, window=vortex_window, positive=True).bfill()
    df["VIM"] = vortex(df, window=vortex_window, positive=False).bfill()
    
    # Verifica se há dados suficientes para comparação (pelo menos 2 linhas)
    if len(df) < 2:
        if verbose:
            print("⚠️ Dados insuficientes para execução da estratégia.")
        return None

    # ------------------------------------------------------------------------
    # 🔄 ANÁLISE E GERAÇÃO DE SINAIS 🔄
    
    # Seleciona os últimos dois registros para comparação
    latest = df.iloc[-1]
    prev   = df.iloc[-2]

    # Condições para COMPRA
    buy_conditions = (
        (latest["VIP"] > latest["VIM"]) and
        (prev["VIP"] < prev["VIM"]) 
    )
    
    # Condições para VENDA
    sell_condition1 = (latest["VIP"] < latest["VIM"])
    sell_condition2 = (prev["SlowS"] > 65)

    # Decisão de negociação
    if sell_condition1 or sell_condition2:    
        trade_decision = False  # Sinal de VENDA
    elif buy_conditions:
        trade_decision = True   # Sinal de COMPRA
    else:
        trade_decision = None

    # ------------------------------------------------------------------------
    # 📝 LOGS E SAÍDA VERBOSA 📝
    
    # Impressão dos dados (verbose)
    if verbose:
        # Presume-se que o índice do DataFrame contenha a data do candle.
        data_candle = latest.name
        if isinstance(data_candle, pd.Timestamp):
            data_candle_str = data_candle.strftime("%d/%m/%Y %H:%M:%S")
        else:
            data_candle_str = str(data_candle)
            
        print("-------")
        print("📊 Estratégia: Indicadores Avançados (Vortex + Outros)")
        print(f" | Candle (index): {data_candle_str}")
        
        # Impressão do campo 'open_time' do DataFrame
        if "open_time" in df.columns:
            open_time_val = latest["open_time"]
            if isinstance(open_time_val, pd.Timestamp):
                open_time_str = open_time_val.strftime("%d/%m/%Y %H:%M:%S")
            else:
                open_time_str = str(open_time_val)
            print(f" | Open Time: {open_time_str}")
        
        print(f" | Fechamento: {latest['close_price']:.3f}")
        print(f" | SlowS({slow_stochastic_smoothing_window}): {latest['SlowS']:.3f}")
        print(f" | VIP(VI+) ({vortex_window}): {latest['VIP']:.3f} (Anterior: {prev['VIP']:.3f})")
        print(f" | VIM(VI-) ({vortex_window}): {latest['VIM']:.3f} (Anterior: {prev['VIM']:.3f})")
        decision_text = "Comprar" if trade_decision else "Vender" if trade_decision is False else "Nenhuma ação"
        print(f" | Decisão: {decision_text}")
        print("-------")
    
    return trade_decision