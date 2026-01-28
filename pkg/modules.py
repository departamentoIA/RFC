# modules.py
import polars as pl
import pandas as pd
import spacy                # Recommended for Spanish
from rapidfuzz import fuzz
import re

csv_file = 'SAT_CFDIS_2018_Emisor'
file_path = './data/' + csv_file + '.csv'
column_names = ['RFC', 'RAZON']
patron_permitido = r'[^a-zA-Z0-9 .,"áéíóúÁÉÍÓÚñÑ]'


def clean_mojibake(texto):
    if not isinstance(texto, str):
        return texto

    # Diccionario de errores comunes (Doble Encoding)
    mapeo = {
        'Ã‘': 'Ñ', 'Ã±': 'ñ',
        'Ã¡': 'á', 'Á ': 'á',
        'Ã©': 'é', 'Ã‰': 'É',
        'Ã­': 'í', 'Ã\xad': 'í',
        'Ã³': 'ó', 'Ã“': 'Ó',
        'Ãº': 'ú', 'Ãš': 'Ú',
        'Ã¼': 'ü', 'Ãœ': 'Ü',
        'Â¿': '¿', 'Â¡': '¡',
        'Ã±': 'ñ',
        'Ã': 'Á',
        'ÃA': 'ÍA',
        'UÃ': 'UÍ',
        'U?A': 'UÑA', 'u?a': 'uÑa'
    }

    for roto, real in mapeo.items():
        texto = texto.replace(roto, real)

    return texto


df_pandas = pd.read_csv(file_path, sep=',', header=0, encoding="utf-8",
                        names=column_names)

# Drop rows with null values
df_pandas = df_pandas.dropna()
rows_ini = df_pandas.shape[0]

df_pandas['RFC_LIMP'] = df_pandas['RFC']
df_pandas['LIMPIO'] = df_pandas['RAZON']

for col in ['RFC_LIMP', 'LIMPIO']:
    df_pandas[col] = df_pandas[col].apply(clean_mojibake)


def tiene_basura(texto):
    if not isinstance(texto, str):
        return False
    # Si encuentra un símbolo que NO está en nuestra lista permitida...
    return bool(pd.Series(texto).str.contains(patron_permitido, regex=True).iloc[0])


"""
df_pandas_final = df_pandas[
    ~df_pandas['LIMPIO'].str.contains(patron_permitido, na=False, regex=True) &
    ~df_pandas['RFC_LIMP'].str.contains(patron_permitido, na=False, regex=True)
].copy()
"""
df_pandas_final = df_pandas
rows_fin = df_pandas_final.shape[0]
print(f"Filas eliminadas: {rows_ini-rows_fin}, de un total de {rows_ini}")
df_pandas_final.to_excel(f"{csv_file}_decodificados_pandas.xlsx", index=False)
"""
# Convert to Polars
df_pandas_final = df_pandas_final[['RFC_LIMP', 'LIMPIO']]
df_pandas_final.columns = ['RFC', 'RAZON']
df = (
    pl.from_pandas(df_pandas_final)
    .filter(pl.col("RFC").is_not_null())    # Filter before processing
    .filter(pl.col("RAZON").is_not_null())
)
print(df.head(5))
print(df.shape)
"""
