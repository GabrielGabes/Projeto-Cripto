from datetime import datetime, timedelta
from random import sample
import calendar

def gerar_blocos_hibridos_2dias(ano_inicio=2024, ano_fim=2025, dias_fixos_por_mes=None, blocos_aleatorios_por_mes=2, seed=None):
    """
    Gera blocos de 2 dias para cada mês no período de ano_inicio até ano_fim,
    combinando blocos fixos e aleatórios.
    
    Parâmetros:
        dias_fixos_por_mes: lista com os dias fixos para cada mês (ex: [1, 10, 20])
        blocos_aleatorios_por_mes: quantidade de blocos aleatórios de 2 dias por mês
        seed: define uma semente aleatória para reprodutibilidade

    Retorna:
        Lista de blocos [[data_inicio, data_fim], ...]
    """
    if dias_fixos_por_mes is None:
        dias_fixos_por_mes = [1, 10, 20]

    if seed is not None:
        import random
        random.seed(seed)

    blocos = []

    for ano in range(ano_inicio, ano_fim + 1):
        for mes in range(1, 13):

            dias_do_mes = calendar.monthrange(ano, mes)[1]
            dias_validos = list(range(1, dias_do_mes - 1))  # para garantir 2 dias de bloco

            # ▪️ Blocos fixos
            for dia in dias_fixos_por_mes:
                if dia + 1 <= dias_do_mes:
                    try:
                        data_inicio = datetime(ano, mes, dia, 0, 0)
                        data_fim = data_inicio + timedelta(days=2)
                        blocos.append([
                            data_inicio.strftime("%d/%m/%Y %H:%M"),
                            data_fim.strftime("%d/%m/%Y %H:%M")
                        ])
                    except:
                        continue

            # ▪️ Blocos aleatórios (sem repetir os dias fixos)
            dias_possiveis = [d for d in dias_validos if d not in dias_fixos_por_mes]
            if len(dias_possiveis) >= blocos_aleatorios_por_mes:
                dias_aleatorios = sample(dias_possiveis, blocos_aleatorios_por_mes)
                for dia in dias_aleatorios:
                    try:
                        data_inicio = datetime(ano, mes, dia, 0, 0)
                        data_fim = data_inicio + timedelta(days=2)
                        blocos.append([
                            data_inicio.strftime("%d/%m/%Y %H:%M"),
                            data_fim.strftime("%d/%m/%Y %H:%M")
                        ])
                    except:
                        continue

    return sorted(blocos, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M"))

# Gera blocos híbridos para 2024 e 2025
intervalos_tempo = gerar_blocos_hibridos_2dias(2024, 2025, dias_fixos_por_mes=[1, 10, 20], blocos_aleatorios_por_mes=2, seed=42)

# Exemplo de exibição
for bloco in intervalos_tempo:
    print(bloco)
