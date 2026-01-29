# globals.py
import re

csv_file = 'pruba'
catalogoRFC = 'CatalogoRFC'
year = 2018

file_path = './data/' + csv_file + '.csv'
catalogo_path = './data/' + catalogoRFC + '.xlsx'
column_names = ['RFC', 'RAZON', 'AÑO']
patron_no_permitido = r'[\\]'

mapeo = {
    'Ã‘': 'Ñ', 'Ã±': 'ñ', 'Ã¡': 'á', 'Á ': 'á', 'Ã©': 'é', 'Ã‰': 'É',
    'Ã­': 'í', 'Ã\xad': 'í', 'Ã³': 'ó', 'Ã“': 'Ó', 'Ãº': 'ú', 'Ãš': 'Ú',
    'Ã¼': 'ü', 'Ãœ': 'Ü', 'Â¿': '¿', 'Â¡': '¡', 'Ã': 'Á', 'ÃA': 'ÍA',
    'UÃ': 'UÍ', r'U\?A': 'UÑA', r'u\?a': 'uÑa', r'\?n$': 'ón', r'\?N$': 'ÓN',
    r'U\#A': 'UÑA', r'u\#a': 'uña', r'lc\?nt': 'lcánt', r'\?LV': 'ÁLV',
    r'r\?ndi': 'réndi'
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
