import pandas as pd


# Estratégia de Antecipação de Média Móvel
def getMovingAverageAntecipationTradeStrategy(
    stock_data: pd.DataFrame, volatility_factor: float, fast_window=7, medium_window=22, slow_window=40, verbose=True
):
    """
    Estratégia avançada de antecipação de movimentos usando três médias móveis.
    Utiliza médias móveis rápida, média e lenta para detectar tendências e antecipações.
    
    Args:
        stock_data: DataFrame com dados de preço
        volatility_factor: Fator de multiplicação da volatilidade para determinar limiares
        fast_window: Tamanho da janela para média móvel rápida
        medium_window: Tamanho da janela para média móvel média 
        slow_window: Tamanho da janela para média móvel lenta
        verbose: Mostrar logs detalhados
        
    Returns:
        bool ou None: True para comprar, False para vender, None para aguardar
    """
    # Garantimos que há dados suficientes antes de calcular as médias móveis
    if len(stock_data) < slow_window:
        if verbose:
            print("❌ Dados insuficientes para calcular médias móveis. Pulando...")
        return None  # Retorna None para evitar erro

    # Criamos cópias das colunas para evitar o warning de Pandas
    stock_data = stock_data.copy()

    # Calcula as Médias Moveis Rápida, Média e Lenta
    stock_data["ma_fast"] = stock_data["close_price"].rolling(window=fast_window).mean()
    stock_data["ma_medium"] = stock_data["close_price"].rolling(window=medium_window).mean()
    stock_data["ma_slow"] = stock_data["close_price"].rolling(window=slow_window).mean()

    # Calcula a volatilidade (desvio padrão) dos preços
    volatility_window = slow_window  # Normalmente é a mesma janela que slow_window da MA strategy.
    stock_data["volatility"] = stock_data["close_price"].rolling(window=volatility_window).std()

    # 🔹 REMOVE LINHAS INICIAIS COM NaN NAS MÉDIAS
    stock_data.dropna(subset=["ma_fast", "ma_medium", "ma_slow"], inplace=True)

    # Se ainda restam poucos dados após remover NaN, pula esse período
    if len(stock_data) < slow_window:
        if verbose:
            print("⚠️ Ainda há poucos dados após remover NaN. Pulando...")
        return None

    # Pega as últimas médias móveis e as anteriores para calcular gradientes
    last_ma_fast = stock_data["ma_fast"].iloc[-1]
    prev_ma_fast = stock_data["ma_fast"].iloc[-3]
    
    last_ma_medium = stock_data["ma_medium"].iloc[-1]
    prev_ma_medium = stock_data["ma_medium"].iloc[-3]
    
    last_ma_slow = stock_data["ma_slow"].iloc[-1]
    prev_ma_slow = stock_data["ma_slow"].iloc[-3]

    # Última volatilidade (evita erro se houver NaN)
    last_volatility = stock_data["volatility"].dropna().iloc[-2] if not stock_data["volatility"].isna().all() else None
    if last_volatility is None:
        return None

    # Calcula os gradientes (taxa de mudança) das médias móveis
    fast_gradient = last_ma_fast - prev_ma_fast
    medium_gradient = last_ma_medium - prev_ma_medium
    slow_gradient = last_ma_slow - prev_ma_slow

    # Calcula as diferenças entre as médias
    fast_medium_diff = abs(last_ma_fast - last_ma_medium)
    medium_slow_diff = abs(last_ma_medium - last_ma_slow)

    # Inicializa a decisão
    ma_trade_decision = None

    # Limiar baseado na volatilidade
    threshold = last_volatility * volatility_factor

    # Toma a decisão com base em todas as médias móveis
    # LÓGICA AVANÇADA: Usa a média média como confirmação e a relação entre os gradientes
    
    # Caso de COMPRA: médias se aproximando por baixo com força suficiente
    if (last_ma_fast < last_ma_medium < last_ma_slow):
        # Verifica se as médias estão convergindo com força (gradientes em ordem crescente)
        if fast_gradient > medium_gradient > slow_gradient:
            # Verifica se a média rápida está próxima o suficiente da média média
            if fast_medium_diff < threshold:
                ma_trade_decision = True  # Comprar
    
    # Caso de VENDA: médias se aproximando por cima com força suficiente
    elif (last_ma_fast > last_ma_medium > last_ma_slow):
        # Verifica se as médias estão convergindo com força (gradientes em ordem decrescente)
        if fast_gradient < medium_gradient < slow_gradient:
            # Verifica se a média rápida está próxima o suficiente da média média
            if fast_medium_diff < threshold:
                ma_trade_decision = False  # Vender

    # Log da estratégia e decisão
    if verbose:
        print("-------")
        print("📊 Estratégia: Moving Average Antecipation")
        print(f" | Última Média Rápida: {last_ma_fast:.3f}")
        print(f" | Última Média Média: {last_ma_medium:.3f}")  # Adicionado log para média móvel média
        print(f" | Última Média Lenta: {last_ma_slow:.3f}")
        print(f" | Última Volatilidade: {last_volatility:.3f}")
        print(f" | Limiar de Antecipação: {threshold:.3f}")
        print(f" | Diferença Fast-Medium: {fast_medium_diff:.3f}")
        print(f" | Diferença Medium-Slow: {medium_slow_diff:.3f}")
        print(f' | Gradiente Rápido: {fast_gradient:.3f} ({ "Subindo" if fast_gradient > 0 else "Descendo" })')
        print(f' | Gradiente Médio: {medium_gradient:.3f} ({ "Subindo" if medium_gradient > 0 else "Descendo" })')  # Adicionado log
        print(f' | Gradiente Lento: {slow_gradient:.3f} ({ "Subindo" if slow_gradient > 0 else "Descendo" })')
        print(f' | Decisão: {"Comprar" if ma_trade_decision == True else "Vender" if ma_trade_decision == False else "Nenhuma"}')
        print("-------")

    return ma_trade_decision
