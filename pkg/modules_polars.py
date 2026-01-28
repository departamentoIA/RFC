# modules.py
import polars as pl
import spacy                # Recommended for Spanish
from rapidfuzz import fuzz

csv_file = 'SAT_CFDIS_2018_Receptor'
file_path = './data/' + csv_file + '.csv'
column_names = ['RFC', 'RAZON']
# patron_permitido = r'[^a-zA-Z0-9 .,"&\+áéíóúÁÉÍÓÚñÑ]'
patron_no_permitido = r'[\#\?\\]'

df = pl.read_csv(
    file_path,
    has_header=True,
    new_columns=column_names,
    encoding="utf8"
)

df = df.drop_nulls()
rows_ini = df.height

# 3. Definir el mapeo de Mojibake para usar con expresiones regulares
# Nota: Algunos caracteres como '?' en Regex deben escaparse con '\\'
mapeo = {
    'Ã‘': 'Ñ', 'Ã±': 'ñ', 'Ã¡': 'á', 'Á ': 'á', 'Ã©': 'é', 'Ã‰': 'É',
    'Ã­': 'í', 'Ã\xad': 'í', 'Ã³': 'ó', 'Ã“': 'Ó', 'Ãº': 'ú', 'Ãš': 'Ú',
    'Ã¼': 'ü', 'Ãœ': 'Ü', 'Â¿': '¿', 'Â¡': '¡', 'Ã': 'Á', 'ÃA': 'ÍA',
    'UÃ': 'UÍ', r'U\?A': 'UÑA', r'u\?a': 'uÑa', r'\?n': 'ón', r'\?N': 'ÓN',
    r'U\#A': 'UÑA', r'u\#a': 'uña'
}


df = df.with_columns([
    pl.col("RFC").alias("RFC_LIMP"),
    pl.col("RAZON").alias("LIMPIO")
])

for roto, real in mapeo.items():
    df = df.with_columns([
        pl.col("RFC_LIMP").str.replace_all(roto, real),
        pl.col("LIMPIO").str.replace_all(roto, real)
    ])

# 5. Filtrar filas que tengan "basura" (caracteres no permitidos)
# En Polars, .str.contains() devuelve un booleano. Usamos .not_() para quedarnos con lo limpio.
df_final = df.filter(
    pl.col("LIMPIO").str.contains(patron_no_permitido).not_() &
    pl.col("RFC_LIMP").str.contains(patron_no_permitido).not_()
)

rows_fin = df_final.height

print(f"Filas eliminadas: {rows_ini - rows_fin}, de un total de {rows_ini}")

df_final.write_excel(f"{csv_file}_decodificados_polars.xlsx")

print(df.shape)
