#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           main.py
Author:         Antonio Arteaga
Last Updated:   2025-01-28
Version:        1.0
Description:    This script obtains all valid RFC and the corresponding name.
Dependencies:   polars==1.37.1, openpyxl==3.1.5, xlsxwriter==3.2.9, spacy==3.8.11,
                RapidFuzz==3.14.3, thefuzz==0.22.1
Usage:          'CatalogoRFC' and 'rfc' are requested to run this script.
Portability:    To make this project executable, run:
pyinstaller --onefile --add-data "pkg/.env;." main.py
"""

from pkg.modules import *
from datetime import datetime

date = datetime.now().strftime("%d/%m/%Y %H:%M")
print(f"Hola {date}")
