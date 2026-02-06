# moral_functions.py
import polars as pl
import spacy                    # Recommended for Spanish
from rapidfuzz import fuzz
from pkg.globals import *


def normalize_tax_regime(df: pl.DataFrame) -> pl.DataFrame:
    """Receive df_moral and normalize tax regime of RFC name.
    Column 'NOMBRE' is created."""
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
    df_fisica.parquet. For df_moral, tax regime of RFC name is normalized and
    column 'NOMBRE' is created."""
    df_fisica = df.filter(pl.col("PERSONA") == "FISICA")
    # df_fisica.write_parquet("df_fisica.parquet")
    print("DataFrame 'fisica' se guardó como df_fisica.parquet temporalmente. "
          "Este DataFrame se procesará posteriormente.")
    df_moral = df.filter(pl.col("PERSONA") == "MORAL")
    return normalize_tax_regime(df_moral)


def process_df_moral(df: pl.DataFrame, file_path: str,
                     catalogo_path: str, proveedoresRiesgoTIC_path: str) -> pl.DataFrame:
    """Receive df_moral and delete all RFC of 'CatalogoRFC' and 'ProveedoresRiesgoTIC'.
    The resulting DataFrame with columns 'RFC', 'NOMBRE' and 'AÑO' is returned."""
    df_catalogoRFC = pl.read_excel(catalogo_path)
    df_proveedores = pl.read_excel(proveedoresRiesgoTIC_path)
    print(f"Procesando DataFrame de personas morales...")
    rows_ini = df.height
    print(f"Filas iniciales = {rows_ini}")

    # Delete RFC of df if they are in catalogs
    df = df.join(df_catalogoRFC, on="RFC", how="anti")
    df = df.join(df_proveedores, on="RFC", how="anti")

    rows_fin = df.height
    print(
        f"Filas duplicadas, es decir, filas contenidas en '{CATALOGO_RFC}' y "
        + f"'{PROVEEDORES_RIESGO_TIC}': {rows_ini - rows_fin}")

    # Extract specific columns
    df = df.select(['RFC', 'NOMBRE', 'AÑO', 'PERSONA'])
    return df


def concat_dfs(df: pl.DataFrame, file_path: str) -> pl.DataFrame:
    """Receive df and concat with the corresponding DataFrame of 'file_path'.
    Both DataFrames should have the same columns. The concated df is sorted
    by column 'RFC' and returned."""
    df_file = pl.read_excel(file_path)

    # Change column type
    df = df.with_columns(pl.col(['AÑO']).cast(pl.Int32, strict=False))
    df_file = df_file.with_columns(
        pl.col(['AÑO']).cast(pl.Int32, strict=False))

    # Concat DataFrames
    df_concated = pl.concat([df, df_file], how="vertical")

    # Sort by 'RFC'
    return df_concated.sort("RFC", descending=False)
