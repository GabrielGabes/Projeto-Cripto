import pandas as pd
import numpy as np

df1 = pd.read_excel("C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/tests/graficos/bck/DADOS_SIMULADOS_1semana.xlsx")
df2 = pd.read_parquet("C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/tests/graficos/bck/DADOS_SIMULADOS_1semana_extra.parquet")
df3 = pd.read_parquet("C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/tests/graficos/DADOS_SIMULADOS_1semana_extra.parquet")

df = pd.concat([df1, df2, df3], axis=0)
df.shape

df.duplicated().sum()

df = df.drop_duplicates().reset_index(drop=True)
df.shape

df.to_parquet("C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/tests/graficos/DADOS_SIMULADOS_1semana_1h_definitivos.parquet", index=False)

for col in df.columns:
    if pd.api.types.is_datetime64tz_dtype(df[col]):
        df[col] = df[col].dt.tz_localize(None)
df.to_excel("C:/Users/gabri/OneDrive/Documentos/Criptos/RoboTraderBinance_1_4b/src/tests/graficos/DADOS_SIMULADOS_1semana_1h_definitivos.xlsx", index=False)
