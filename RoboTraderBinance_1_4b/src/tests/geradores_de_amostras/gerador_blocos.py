from datetime import datetime, timedelta

def gerar_blocos_sistematicos_2dias(ano_inicio=2024, ano_fim=2025, blocos_fixos_por_mes=None):
    """
    Gera blocos sistemáticos de 2 dias para cada mês entre ano_inicio e ano_fim.
    
    Cada mês conterá blocos nos dias pré-definidos (ou padrão):
    [1, 5, 10, 15, 25]
    
    Retorna uma lista de listas com pares [data_inicio, data_fim]
    """
    blocos = []

    # Dias fixos para criar os blocos de 2 dias
    if blocos_fixos_por_mes is None:
        blocos_fixos_por_mes = [1, 5, 10, 15, 25]

    for ano in range(ano_inicio, ano_fim + 1):
        for mes in range(1, 13):
            for dia in blocos_fixos_por_mes:
                try:
                    data_inicio = datetime(ano, mes, dia, 0, 0)
                    data_fim = data_inicio + timedelta(days=2)
                    
                    # Garantir que o mês não está estourando (ex: 30 → 32 jan)
                    if data_fim.month != mes and data_fim.day < 3:
                        continue

                    bloco = [
                        data_inicio.strftime("%d/%m/%Y %H:%M"),
                        data_fim.strftime("%d/%m/%Y %H:%M")
                    ]
                    blocos.append(bloco)
                except:
                    continue  # Ignora datas inválidas (ex: dia 30 em fevereiro)

    return blocos

# Gera blocos para 2024 e 2025
intervalos_tempo = gerar_blocos_sistematicos_2dias()
# Exemplo de impressão dos primeiros blocos
for i in intervalos_tempo:
    print(i)
