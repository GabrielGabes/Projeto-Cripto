import os
import re

# Caminho da pasta onde estão os arquivos .py
pasta = "C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/strategies/extras"

# Mapeamento de substituição
substituicoes = {
    "close": "close_price",
    "open": "open_price",
    "high": "high_price",
    "low": "low_price"
}

# Regex para encontrar as palavras entre aspas, sem _price depois
regex_base = r"(?<!_)(['\"])(?P<palavra>{})\1"

# Processa cada arquivo
for nome_arquivo in os.listdir(pasta):
    if not nome_arquivo.endswith(".py"):
        continue

    caminho_completo = os.path.join(pasta, nome_arquivo)

    with open(caminho_completo, "r", encoding="utf-8") as f:
        conteudo = f.read()

    conteudo_modificado = conteudo

    # Aplica todas as substituições
    for palavra, nova in substituicoes.items():
        regex = regex_base.format(palavra)
        conteudo_modificado = re.sub(
            regex,
            lambda m: f"{m.group(1)}{nova}{m.group(1)}",  # mantém as aspas originais
            conteudo_modificado
        )

    # Só sobrescreve se houver mudança
    if conteudo != conteudo_modificado:
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(conteudo_modificado)
        print(f"✔️ Corrigido: {nome_arquivo}")
    else:
        print(f"✅ Nenhuma mudança: {nome_arquivo}")
