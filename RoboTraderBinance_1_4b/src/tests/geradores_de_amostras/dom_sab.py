from datetime import datetime, timedelta

def gerar_domingo_sabado_semanas_ano(ano=2025):
    """
    Gera uma lista de [domingo, sábado] para cada semana do ano especificado,
    limitando a saída até o dia anterior ao dia atual.
    
    Retorna:
        Lista de listas: [['05/01/2025', '11/01/2025'], ...]
    """
    semanas = []
    hoje = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    limite = hoje - timedelta(days=1)

    # Começa no primeiro domingo do ano
    data = datetime(ano, 1, 1)
    while data.weekday() != 6:  # 6 = domingo
        data += timedelta(days=1)
    
    # Gera blocos semanais até o final do ano ou até ontem
    while data.year == ano:
        domingo = data
        sabado = data + timedelta(days=6)

        # Limita até ontem
        if sabado > limite:
            break

        semanas.append([
            domingo.strftime("%d/%m/%Y") + ' 00:00',
            sabado.strftime("%d/%m/%Y") + ' 00:00'
        ])

        data += timedelta(weeks=1)

    return semanas

# # Mostrar as 5 primeiras semanas
# for semana in gerar_domingo_sabado_semanas_ano(2025):
#     print(semana)