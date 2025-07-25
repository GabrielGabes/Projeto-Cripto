import requests
import time
import datetime
from consulta_tendencias import consulta
from price_variation import build_variation_table
import threading

#================================================================================# Configurações do bot de status
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

timer_status = None  # variável global para controlar o timer

def verificar_status_robo():
    global timer_status
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem = f"RPA INDICADORES DIARIOS: Online {agora} ✅"
    send_status_message(mensagem)

    intervalo = obter_intervalo_do_info()
    timer_status = threading.Timer(intervalo, verificar_status_robo)
    timer_status.start()
    
#================================================================================
# Substitua pelos seus valores
TELEGRAM_BOT_TOKEN = "7446801344:AAHenxPWZzBffuowmaTWISyksUIsvBltkIg"
CHAT_ID = "-4628628345"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)
#================================================================================
verificar_status_robo()

# Loop para executar todo primeiro minuto após a virada de hora (exemplo: 01:01, 02:01, etc.)
while True:
    now = datetime.datetime.now()
    if now.minute == 1 and now.second < 5:  # Executa entre 01:01:00 e 01:01:05 para segurança
        try:
            message = consulta()
            send_telegram_message(message)

            message2 = build_variation_table()
            send_telegram_message(message2)

            print(f"Mensagens enviadas ao Telegram às {now.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Erro ao executar consultas ou enviar mensagens: {e}")
            message = f"Erro ao executar consultas ou enviar mensagens: {e}"
            send_telegram_message(message)
             # Cancela o timer do status
            if timer_status:
                timer_status.cancel()
            # Finaliza o programa
            break
        time.sleep(60)  # Espera 1 minuto para evitar execução dupla
    else:
        time.sleep(90)  # Checa a cada 5 segundos até chegar o momento certo