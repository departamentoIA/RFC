#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           main.py
Author:         Antonio Arteaga
Last Updated:   2025-01-28
Version:        1.0
Description:    This script obtains all valid RFC and the corresponding name.
Dependencies:   polars==1.37.1, openpyxl==3.1.5, xlsxwriter==3.2.9, spacy==3.8.11,
                RapidFuzz==3.14.3, thefuzz==0.22.1, 

Usage:          'CatalogoRFC', 'PROVEEDORES_RIESGO_TIC', 'RFC_MORAL', 'RFC_FISICA' and
                the file with new RFC are requested. SLM should be installed:
                pip install "./model/es_core_news_sm-3.8.0-py3-none-any.whl" or
                python -m spacy download es_core_news_sm
Portability:    To make this project executable, run:
pyinstaller --onefile --add-data "pkg/.env;." main.py
"""

from pkg.modules import *
from pkg.moral_functions import *


df_decodificado = encode_df(file_path)
df = validate_RFC_and_set_year(df_decodificado)
# try_write_excel(df, csv_file, "validado")
df_moral_completo = get_df_moral_and_save_df_fisica(df)
# try_write_excel(df_moral_completo, csv_file, "moral_completo")
df_moral = process_df_moral(
    df_moral_completo, file_path, catalogo_path, proveedoresRiesgoTIC_path)
# try_write_excel(df_moral, csv_file, "moral_procesado")

df_lemmatizado = lemmatization(df_moral)
try_write_excel(df_lemmatizado, csv_file, "moral_lematizado")

df_moral_concatenado = concat_dfs(df_lemmatizado, catalogo_moral_path)
try_write_excel(df_moral_concatenado, csv_file, "moral_concatenado")
