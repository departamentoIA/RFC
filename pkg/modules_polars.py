# modules.py
import polars as pl
import spacy                # Recommended for Spanish
from rapidfuzz import fuzz
import re
csv_file = 'pruba'
catalogoRFC = 'CatalogoRFC'
year = 2018

file_path = './data/' + csv_file + '.csv'
catalogo_path = './data/' + catalogoRFC + '.xlsx'
column_names = ['RFC', 'RAZON', 'AÑO']
patron_no_permitido = r'[\#\?\\]'

mapeo = {
    'Ã‘': 'Ñ', 'Ã±': 'ñ', 'Ã¡': 'á', 'Á ': 'á', 'Ã©': 'é', 'Ã‰': 'É',
    'Ã­': 'í', 'Ã\xad': 'í', 'Ã³': 'ó', 'Ã“': 'Ó', 'Ãº': 'ú', 'Ãš': 'Ú',
    'Ã¼': 'ü', 'Ãœ': 'Ü', 'Â¿': '¿', 'Â¡': '¡', 'Ã': 'Á', 'ÃA': 'ÍA',
    'UÃ': 'UÍ', r'U\?A': 'UÑA', r'u\?a': 'uÑa', r'\?n': 'ón', r'\?N': 'ÓN',
    r'U\#A': 'UÑA', r'u\#a': 'uña'
}

# Regular expressions
RFC_FISICA_REGEX = re.compile(
    r"^[A-ZÑ&]{4}"
    r"\d{2}(0[1-9]|1[0-2])"
    r"(0[1-9]|[12]\d|3[01])"
    r"[A-Z0-9]{3}$"
)

RFC_MORAL_REGEX = re.compile(
    r"^[A-ZÑ&]{3}"
    r"\d{2}(0[1-9]|1[0-2])"
    r"(0[1-9]|[12]\d|3[01])"
    r"[A-Z0-9]{3}$"
)


def encode_df(file_path: str) -> pl.DataFrame:
    """Read file to get a Dataframe with manual encoding"""
    df = pl.read_csv(
        file_path,
        has_header=True,
        new_columns=column_names[0:2],
        encoding="utf8"
    )

    df = df.drop_nulls()
    rows_ini = df.height
    # Change column types
    df = df.with_columns(
        pl.col([column_names[0], column_names[1]]).cast(
            pl.String, strict=False)
    )
    # Create columns
    df = df.with_columns([
        pl.col("RFC").alias("RFC_LIMP"),
        pl.col("RAZON").alias("LIMPIO")
    ])

    for roto, real in mapeo.items():
        df = df.with_columns([
            pl.col("RFC_LIMP").str.replace_all(roto, real),
            pl.col("LIMPIO").str.replace_all(roto, real)
        ])

    # Filter according to allowed pattern
    df_final = df.filter(
        pl.col("LIMPIO").str.contains(patron_no_permitido).not_() &
        pl.col("RFC_LIMP").str.contains(patron_no_permitido).not_()
    )

    rows_fin = df_final.height
    print(
        f"Filas eliminadas en decodificación: {rows_ini - rows_fin}, de un total de {rows_ini}")
    # df_final.write_excel(f"{csv_file}_decodificado.xlsx")

    # Extract specific columns
    df = df_final.select(['RFC_LIMP', 'LIMPIO'])
    df = df.rename({'RFC_LIMP': 'RFC', 'LIMPIO': 'RAZON'})
    # df.write_excel(f"{csv_file}_decodificado.xlsx")
    return df


def get_df_with_3_cols(file_path: str, catalogo_path: str) -> pl.DataFrame:
    """Construct a DataFrame with columns 'RFC', 'RAZON' and 'AÑO',
    after manual encoding and RFC substraction"""
    df = encode_df(file_path)
    catalogo = pl.read_excel(catalogo_path)

    # Delete RFC of df if they are in catalogo
    df = df.join(catalogo, on="RFC", how="anti")
    # df.write_excel(f"{csv_file}_filtrado.xlsx")

    # Add year
    df = df.with_columns(pl.lit(year).alias(column_names[2]))
    # print(df.head())
    return df


df = get_df_with_3_cols(file_path, catalogo_path)
"""

"""
