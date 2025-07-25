#!/usr/bin/env python
# coding: utf-8

#================================================================================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import requests
import time
import datetime

import threading
import pandas as pd
import numpy as np

#ignorando Warning inuteis
import warnings 
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.filterwarnings(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

import traceback
import platform

# import schedule

#================================================================================
chrome_options = Options()
# chrome_options.add_argument("--headless")  # remove se quiser ver o navegador
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # Desativa o isolamento de processos (necess�rio em ambientes restritos, como Raspberry Pi ou Docker)
chrome_options.add_argument("--disable-dev-shm-usage") # Redireciona o uso de mem�ria compartilhada (evita erros em sistemas com /dev/shm limitado)
# chrome_options.add_argument("--disable-infobars") # Remove a barra "Chrome est� sendo controlado por software automatizado"
chrome_options.add_argument("--disable-extensions") # Impede que extens�es do Chrome sejam carregadas (torna o navegador mais limpo e leve)
chrome_options.add_argument("--window-size=1366x768") # Define o tamanho da janela: largura=1366, altura=768 (simula tela de notebook comum)
# chrome_options.add_argument("--window-position=0,312") # Posiciona a janela na tela: canto inferior (0 = esquerda, 312 = parte inferior da tela)


if platform.system() == "Windows":
    # Usar webdriver-manager no Windows
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
else:
    # Usar driver manual no Linux/Raspberry
    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=chrome_options
    )
print('Iniciando o navegador...'); time.sleep(5)

#================================================================================

BOT_TOKEN_STATUS = '8013077654:AAFWFkaRcWDCRHcCSXbjn877CNs9wQ4hmBA'
CHAT_ID_STATUS = '-1002871039327'

def send_status_message(mensagem):
    print('Bot online ✅')
    url = f"https://api.telegram.org/bot{BOT_TOKEN_STATUS}/sendMessage"
    payload = {
        'chat_id': CHAT_ID_STATUS,
        'text': mensagem,
        'parse_mode': 'Markdown' 
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem: {response.text}")
    except Exception as e:
        print(f"Exceção ao enviar mensagem: {e}")

def obter_intervalo_do_info():
    url = f"https://api.telegram.org/bot{BOT_TOKEN_STATUS}/getChat"
    params = {'chat_id': CHAT_ID_STATUS}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            descricao = data.get('result', {}).get('description', '')
            intervalo = float(descricao.strip()) * 60  # minutos para segundos
            intervalo = max(1, int(intervalo))  # garante pelo menos 1 segundo
            print(f"Intervalo lido da descrição: {intervalo} seg")
            return intervalo
        else:
            print(f"Erro ao obter descrição: {response.text}")
    except Exception as e:
        print(f"Erro ao ler info: {e}")
    return 600  # valor padrão em segundos (10 minutos)

timer_status = None

def verificar_status_robo():
    global timer_status
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem = f"RPA ACOMPANHANEWS: Online {agora} ✅"
    send_status_message(mensagem)

    intervalo = obter_intervalo_do_info()
    timer_status = threading.Timer(intervalo, verificar_status_robo)
    timer_status.start()

#================================================================================
def buscar_noticias(termo_busca, intervalo="1h"):
    # opções de intervalo 
    # 'Última hora':'1h',
    # 'Últimas 24 horas': '1d',
    # 'Última semana':'7d',
    termo_url = termo_busca.replace(" ", "%20")
    url = f"https://news.google.com/search?q={termo_url}%20when%3A{intervalo}&hl=pt-BR&gl=BR&ceid=BR%3Apt-419"
    driver.get(url)

#================================================================================
def extrair_noticias():
    # Pega o HTML da página e processa com BS4
    html = driver.find_element("xpath", "/html").get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")
    resultados = []

    for artigo in soup.select("article"):
        try:
            # Título e link
            a_tag = artigo.select_one("a.JtKRv")
            if not a_tag:
                continue
            titulo = a_tag.get_text(strip=True)
            link = a_tag.get("href")
            if link.startswith("./"):
                link = "https://news.google.com" + link[1:]

            # Site de origem
            site_elem = artigo.select_one("div.vr1PYe")
            site = site_elem.get_text(strip=True) if site_elem else "Site desconhecido"

            # Tempo publicado
            tempo_elem = artigo.select_one("time.hvbAAd")
            tempo_texto = tempo_elem.get_text(strip=True) if tempo_elem else "Tempo não disponível"
            tempo_data = tempo_elem.get("datetime") if tempo_elem and tempo_elem.has_attr("datetime") else None

            resultados.append({
                "titulo": titulo,
                "site": site,
                "tempo": tempo_texto,
                "data_iso": tempo_data,
                "link": link
            })

        except Exception as e:
            continue

    return resultados

#================================================================================
def formatar_linha_estilo_telegram(df, linha):
    dados = df.iloc[linha]

    return (
        f"<b>📰 {dados['titulo']}</b>\n"
        f"<b>🌐 Site:</b> {dados['site']}\n"
        f"<b>⏱ Tempo:</b> {dados['tempo']}\n"
        f"<b>📅 Data ISO:</b> {dados['data_iso']}\n"
        f"<a href=\"{dados['link']}\">🔗 Link</a>"
    )

# Substitua pelos seus valores
TELEGRAM_BOT_TOKEN = "7446801344:AAHenxPWZzBffuowmaTWISyksUIsvBltkIg"
CHAT_ID = "-4628628345"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
            "chat_id": CHAT_ID, 
            "text": message,
            "parse_mode": "HTML",
            # disable_web_page_preview=True  # opcional: oculta o preview do link
            }
    requests.post(url, data=data)

#================================================================================
if platform.system() == "Windows":
    # caminho_fd = 'C:/Users/gabri/OneDrive/Documentos/Cripto/AcompanhaNews/' #-PC GABRIEL-#
    caminho_fd = 'C:/Users/michael/OneDrive/Documentos/Criptos/AcompanhaNews/' #- PC MICHAEL-#
else:
    caminho_fd = '/home/maikola/Documentos/Projeto-Cripto-main/AcompanhaNews/'
fd = pd.read_csv(caminho_fd + 'registros_noticias.csv', sep=';')

def pesquisa_completa(pesquisa, periodo='1h'):
    global fd  # adiciona essa linha
    
    buscar_noticias(pesquisa, periodo)
    time.sleep(3)
    noticias = extrair_noticias()

    if noticias == []:
        pass
    else:
        df = pd.DataFrame(noticias)
        df['pesquisa'] = pesquisa

        # verificando se já há registro desta noticia no sistema
        for linha in range(len(df)):
            filtro = (fd['titulo'] == df['titulo'][linha]) & (fd['site'] == df['site'][linha])
            if len(fd[filtro]) >= 1:
                df = df.drop(linha, axis=0)

        df = df.reset_index(drop=True)
        
        # se ainda sobrar alguma noticia, mande mensagem para o telegram
        if len(df) > 0:
            mensagem_final = ''
            fd = pd.concat([fd, df], axis=0).reset_index(drop=True)
            for linha in df.index:
                    mensagem = formatar_linha_estilo_telegram(df, linha)
                    mensagem_final = mensagem_final + '\n' + '*'*40 + '\n' + mensagem
            send_telegram_message(mensagem_final)

#================================================================================
def salvando_planilha_registros():
    fd.to_csv('registros_noticias.csv', sep=';', index=False)

def aviso_vida():
    send_telegram_message('***********************************')
#================================================================================

# Função para pesquisar por todos os termos
def rodar_pesquisas():
    # Lista de termos de pesquisa
    termos_de_pesquisa = [
        'Algorand (ALGO) crypto',
        'Near Protocol (NEAR) crypto',
        'Flow (FLOW) crypto',
        'Kadena (KDA) crypto',
        'HBAR (Hedera Hashgraph) crypto',
        'Oasis Network (ROSE) crypto',
        'Ocean Protocol (OCEAN) crypto',
        'Arweave (AR) crypto',
        'Celo (CELO) crypto',
        'Radix (XRD) crypto',
        'Ergo (ERG) crypto',
        'Akash Network (AKT) crypto',
        'Constellation (DAG) crypto',
        'KILT Protocol (KILT) crypto',
        'Secret Network (SCRT) crypto',
        'Velas (VLX) crypto'
    ]
    for termo in termos_de_pesquisa:
        print('Pesquisando:', termo)
        pesquisa_completa(termo)  # Sua função que busca as notícias
        time.sleep(1)
# Testando
# pesquisa_completa('BTC'); time.sleep(2)
#===============================================================================

verificar_status_robo()

while True:
    try:
        rodar_pesquisas()
        time.sleep(60*5)
    except:
        mensagem = 'erro fatal! o código foi encerrado.\n' + traceback.format_exc()
        send_telegram_message(mensagem)
        if timer_status:
            timer_status.cancel()
        exit(1)


#===============================================================================
# Agendamentos
# schedule.every(5).minutes.do(lambda: pesquisa_completa('cryptos'))
# schedule.every(4).minutes.do(rodar_pesquisas)
# schedule.every().hour.at(":00").do(salvando_planilha_registros)

# # Loop principal
# print('Entrando em Looping...'); time.sleep(2)
# while True:
#     schedule.run_pending()  # Executa a próxima função agendada, se houver
#     time.sleep(1)           # Aguarda 1 segundo antes de verificar novamente

# #===============================================================================