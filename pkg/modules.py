# modules.py
import polars as pl
import spacy                    # Recommended for Spanish
from rapidfuzz import fuzz
from pkg.globals import *


def try_write_excel(df: pl.DataFrame, file: str, status="") -> None:
    """Try to write in Excel file."""
    try:
        df.write_excel(f"{file}_{status}.xlsx")
    except:
        print("\n\nNo puedo escribir en el excel si está abierto!")


def encode_df(file_path: str) -> pl.DataFrame:
    """Read file to get a cleaned Dataframe applying manual encoding"""
    df = pl.read_csv(
        file_path,
        has_header=False,
        new_columns=column_names[0:2],
        encoding="utf8"
    )
    df = df.drop_nulls()
    rows_ini = df.height
    print(f"Decodificando {file_path}...")
    # Change column types and create columns
    df = df.with_columns(
        pl.col(column_names[0]).cast(pl.String, strict=False),
        pl.col(column_names[1]).cast(pl.String, strict=False),
        pl.col("RFC").alias("RFC_LIMP"),
        pl.col("RAZON").alias("LIMPIO")
    )

    # To uppercase
    rfc_expr = pl.col("RFC_LIMP").str.to_uppercase()
    limpio_expr = pl.col("LIMPIO").str.to_uppercase()

    # To uppercase and replace
    for roto, real in mapeo.items():
        rfc_expr = rfc_expr.str.replace_all(roto, real)
        limpio_expr = limpio_expr.str.replace_all(roto, real)

    # Replace '?\"' by " " and delete double blanks
    rfc_expr = (
        rfc_expr.str.replace_all(r'[?\\"]', " ")
        .str.replace_all(r"\s+", " ")
        .str.strip_chars()
    )
    limpio_expr = (
        limpio_expr.str.replace_all(r'[?\\"*]', " ")
        .str.replace_all(r"\s+", " ")
        .str.strip_chars()
    )

    # Apply changes
    df_final = df.with_columns([
        rfc_expr,
        limpio_expr
    ])

    # Filter according to allowed pattern
    df_final = df_final.filter(
        (pl.col("LIMPIO").str.contains(allowed_pattern))
    )

    rows_fin = df_final.height
    print(
        f"Filas eliminadas en decodificación: {rows_ini - rows_fin}, de un total de {rows_ini}")
    try_write_excel(df_final, csv_file, "decodificado")

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


def normalize_tax_regime(df: pl.DataFrame) -> pl.DataFrame:
    """Receive df_moral and normalize tax regime of RFC.
    Column 'NOMBRE' is added."""
    # Normalize "RAZON"
    normalize_text = (
        pl.col(column_names[1])
        .cast(pl.String)
        .str.strip_chars(".,; ")
        .str.replace_all(r"[,;.]", "")
        .str.to_uppercase()
    )

    for pattern, replacement in norm_rules:
        normalize_text = normalize_text.str.replace_all(pattern, replacement)

    normalize_text = (
        normalize_text.str.replace_all(r'[/\-]', ' ')
        .str.replace_all(r'\s+', ' ')
        .str.strip_chars()
    )
    return df.with_columns(normalize_text.alias("NOMBRE"))


def get_df_moral_and_save_df_fisica(df: pl.DataFrame) -> pl.DataFrame:
    """Receive the full df, divide it into 'moral' and 'fisica', df_fisica is saved as
    df_fisica.parquet. For df_moral, tax regime of RFC is normalized and
    column 'NOMBRE' is created."""
    df_fisica = df.filter(pl.col("PERSONA") == "FISICA")
    df_fisica.write_parquet("df_fisica.parquet")
    print("DataFrame 'fisica' se guardó como df_fisica.parquet")
    df_moral = df.filter(pl.col("PERSONA") == "MORAL")
    return normalize_tax_regime(df_moral)


def process_df_moral(df: pl.DataFrame, file_path: str, catalogo_path: str, proveedoresRiesgoTIC_path: str) -> pl.DataFrame:
    """Receive df_moral and delete all RFC of 'CatalogoRFC' and 'ProveedoresRiesgoTIC'.
    Columns are 'RFC', 'NOMBRE' and 'AÑO'."""
    df_catalogoRFC = pl.read_excel(catalogo_path)
    df_proveedores = pl.read_excel(proveedoresRiesgoTIC_path)

    rows_ini = df.height
    print(f"Filas iniciales = {rows_ini}")

    # Delete RFC of df if they are in catalogo
    df = df.join(df_catalogoRFC, on="RFC", how="anti")
    df = df.join(df_proveedores, on="RFC", how="anti")
    # df.write_excel(f"{csv_file}_filtrado.xlsx")

    rows_fin = df.height
    print(
        f"Filas duplicadas del 'catalogoRFC': {rows_ini - rows_fin}, de un total de {rows_ini}")

    # print(df.head())
    return df
