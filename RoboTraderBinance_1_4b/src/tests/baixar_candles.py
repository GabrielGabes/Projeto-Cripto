from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

# Carrega credenciais do .env
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")
client = Client(api_key, secret_key)

def baixar_candles(cod_moeda: str, 
                   data_inicio: str, 
                   data_fim: str, 
                   periodo: str, 
                   ajuste=True) -> pd.DataFrame:
    """
    Baixa candles de um par de moedas entre duas datas-hora com o período especificado,
    usando requisições paginadas (500 por vez) e ajuste de 120 candles anteriores para cálculo de indicadores.
    """

    # Converte período para timedelta
    def periodo_para_timedelta(p):
        unidade = p[-1]
        valor = int(p[:-1])
        if unidade == 'm':
            return timedelta(minutes=valor)
        elif unidade == 'h':
            return timedelta(hours=valor)
        elif unidade == 'd':
            return timedelta(days=valor)
        else:
            raise ValueError(f"Período '{p}' não reconhecido (use '1m', '15m', '1h', etc)")

    # Converte string para datetime com fuso de São Paulo
    def str_para_datetime(data_str):
        dt = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
        return pytz.timezone("America/Sao_Paulo").localize(dt)

    # Datas de início e fim com ajuste de buffer se necessário
    dt_inicio = str_para_datetime(data_inicio)
    dt_fim = str_para_datetime(data_fim)
    delta = periodo_para_timedelta(periodo)

    if ajuste:
        dt_inicio_ajustado = dt_inicio - (delta * 120)
    else:
        dt_inicio_ajustado = dt_inicio

    ts_inicio = int(dt_inicio_ajustado.timestamp() * 1000)
    ts_fim = int(dt_fim.timestamp() * 1000)
    max_candles = 500

    candles_total = []
    # print(f"⏳ Iniciando download de candles para {cod_moeda} de {dt_inicio.strftime('%d/%m/%Y %H:%M')} até {dt_fim.strftime('%d/%m/%Y %H:%M')}...")

    while True:
        ts_fim_lote = ts_inicio + int(delta.total_seconds() * 1000 * max_candles)

        candles = client.get_klines(
            symbol=cod_moeda,
            interval=periodo,
            startTime=ts_inicio,
            endTime=min(ts_fim_lote, ts_fim)
        )

        if not candles:
            break

        candles_total.extend(candles)

        ultimo_candle_time = candles[-1][0]
        ts_inicio = ultimo_candle_time + int(delta.total_seconds() * 1000)

        # Interrompe se passou da data final real (não do buffer)
        if ts_inicio > ts_fim:
            break

    # if not candles_total:
    #     # print("⚠️ Nenhum dado retornado.")
    #     return pd.DataFrame()

    # Monta o DataFrame
    df = pd.DataFrame(candles_total, columns=[
        "open_time", "open_price", "high_price", "low_price", "close_price", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms").dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")

    df[["open_price", "high_price", "low_price", "close_price", "volume"]] = \
        df[["open_price", "high_price", "low_price", "close_price", "volume"]].astype(float)

    # print(f"✅ Candles baixados: {len(df)}")
    # print(f"🕒 Intervalo real: {df['open_time'].min()} ➝ {df['open_time'].max()}")

    return df[["close_price", "open_time", "open_price", "high_price", "low_price", "volume"]]

### TESTANDO
# NOME_MOEDA = 'BTC'
# STOCK_CODE = NOME_MOEDA  # Código da Criptomoeda
# OPERATION_CODE = NOME_MOEDA + "USDT"  # Código da operação (cripto + moeda)
# INITIAL_BALANCE = 1000  # Valor de investimento inicial em USDT ou BRL
# CANDLE_PERIOD = '1h'

# intervalos_tempo = ['15/07/2025 00:00', '20/07/2025 00:00']
# baixar_candles(OPERATION_CODE, intervalos_tempo[0], intervalos_tempo[1], CANDLE_PERIOD)