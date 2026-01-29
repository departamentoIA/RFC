# modules.py
import polars as pl
import spacy                # Recommended for Spanish
from rapidfuzz import fuzz
from pkg.globals import *


def encode_df(file_path: str) -> pl.DataFrame:
    """Read file to get a Dataframe with manual encoding"""
    df = pl.read_csv(
        file_path,
        has_header=False,
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
    df_final.write_excel(f"{csv_file}_decodificado.xlsx")

    # Extract specific columns
    df = df_final.select(['RFC_LIMP', 'LIMPIO'])
    df = df.rename({'RFC_LIMP': 'RFC', 'LIMPIO': 'RAZON'})
    return df


def validate_RFC_and_set_year(df: pl.DataFrame) -> pl.DataFrame:
    """Receive an encoded DataFrame, normalize RFC and delete invalid RFC.
    Then, column 'PERSONA' is added, corresponding to 'FISICA' or 'MORAL',
    and column 'AÑO' is also added."""
    # Normalize RFC
    df = df.with_columns(
        pl.col("RFC").str.strip_chars().str.strip_chars('.')
        .str.strip_chars().str.to_uppercase()
    )
    # Classify according to tax regime
    df = (
        df.with_columns(
            pl.when(pl.col("RFC").str.contains(RFC_FISICA_REGEX.pattern if hasattr(
                RFC_FISICA_REGEX, 'pattern') else RFC_FISICA_REGEX))
            .then(pl.lit("FISICA"))
            .when(pl.col("RFC").str.contains(RFC_MORAL_REGEX.pattern if hasattr(RFC_MORAL_REGEX, 'pattern') else RFC_MORAL_REGEX))
            .then(pl.lit("MORAL"))
            .otherwise(None)
            .alias("PERSONA")
        )
        .filter(pl.col("PERSONA").is_not_null())
    )
    # Add year
    df = df.with_columns(pl.lit(year).alias(column_names[2]))
    return df


'''
def process_df_moral(file_path: str, catalogo_path: str) -> pl.DataFrame:
    """Construct a DataFrame with columns 'RFC', 'RAZON' and 'AÑO',
    after manual encoding and RFC substraction"""
    # df = normalize_RFC(file_path)
    catalogo = pl.read_excel(catalogo_path)

    rows_ini = df.height
    print(f"Filas iniciales = {rows_ini}")

    # Delete RFC of df if they are in catalogo
    df = df.join(catalogo, on="RFC", how="anti")
    # df.write_excel(f"{csv_file}_filtrado.xlsx")

    rows_fin = df.height
    print(
        f"Filas duplicadas del 'catalogoRFC': {rows_ini - rows_fin}, de un total de {rows_ini}")

    # print(df.head())
    return df
'''
