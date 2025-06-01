def calculadora_candles(formato, saida="semana"):
    """
    Calcula a quantidade de candles em um determinado período (mês, semana ou dia).
    
    :param formato: String indicando o intervalo (ex: '1m', '5m', '1h', '1d', '1w')
    :param saida: Define o período da saída ('mes', 'semana' ou 'dia'). Padrão: 'mes'
    :return: Número de candles no período desejado
    """

    # Mapeamento da conversão para um mês (4 semanas)
    conversao = {
        'm': 60 * 24 * 7 * 4,  # Minutos → candles por mês
        'h': 24 * 7 * 4,       # Horas → candles por mês
        'd': 7 * 4,            # Dias → candles por mês
        'w': 4                 # Semanas → candles por mês
    }
    
    try:
        tempo = int(formato[:-1])  # Extrai a parte numérica
        unidade = formato[-1]      # Extrai a unidade (m, h, d, w)

        if unidade in conversao:
            candles_por_mes = conversao[unidade] / tempo  # Cálculo base (candles por mês)

            # Ajuste para diferentes saídas
            if saida == "mes":
                return int(candles_por_mes)
            elif saida == "semana":
                return int(candles_por_mes / 4)
            elif saida == "dia":
                return int(candles_por_mes / 28)  # Aproximadamente 28 dias por mês
            else:
                raise ValueError("Tipo de saída inválido! Escolha entre 'mes', 'semana' ou 'dia'.")
        
        else:
            raise ValueError("Formato inválido! Use 'm', 'h', 'd' ou 'w'.")
    
    except ValueError as e:
        return f"Erro: {e}"

'''
# Exemplos de uso:
entradas = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '1w']
tipos_saida = ['mes', 'semana', 'dia']

# Teste para todas as combinações de entrada e saída
for entrada in entradas:
    for tipo in tipos_saida:
        print(f"{entrada} ({tipo}): {calculadora_candles(entrada, tipo)} candles")
    print('='*30)
'''