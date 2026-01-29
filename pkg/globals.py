# globals.py
import re

csv_file = 'SAT_CFDIS_2020_Emisor'
catalogoRFC = 'CatalogoRFC'
year = 2020

file_path = './data/' + csv_file + '.csv'
catalogo_path = './data/' + catalogoRFC + '.xlsx'
column_names = ['RFC', 'RAZON', 'AÑO']
patron_no_permitido = r'[\\]'

mapeo = {
    r'ACU\#A': 'ACUÑA', r'ACU\?A': 'ACUÑA', r'CU\?A': 'CUAÑA',
    r'ACUÃ\?A': 'ACUÑA', r'BOLA\?OS': 'BOLAÑOS', r'A\?UELO': 'AÑUELO',
    r'AVENDA\?O': 'AVENDAÑO',  r'NIER\?A': 'NIERÍA',
    r'ALC\?NT': 'ALCÁNT', r'\?LV': 'ÁLV', r'R\?NDI': 'RÉNDI',
    r'CI\?N\s': 'CIÓN ', r'MAR\?A': 'MARÍA', r'GR\?A': 'GRÍA',
    r'JOS\?': 'JOSÉ', r'BEN\?TEZ': 'BENÍTEZ', r'CUAUHT\?MOC': 'CUAUHTÉMOC',
    r'COMPA\?IA': 'COMPAÑÍA', r'\?NGEL': 'ÁNGEL', r'CI\?N$': 'CIÓN',
    r'BRISE\?O': 'BRISEÑO',  r'ALAN\?S': 'ALANÍS', r'MARTÃ\?NEZ': 'MARTÍNEZ',
    r'AVI\?A': 'AVIÑA', r'G\?N\s': 'GÓN ', r'ALBARR\?N': 'ALBARRÁN',
    r'AR\?VALO': 'ARÉVALO', r'BA\?OS': 'BAÑOS', r'BRISE\?O': 'BRISEÑO',
    r'CASTA\?EDA': 'CASTAÑEDA', r'AGUI\?IGA': 'AGUIÑIGA', r'ALCAL\?': 'ALCALÁ',
    r'ADRI\?N': 'ADRIÁN', r'BARRAG\?N': 'BARRAGÁN', r'BELTR\?N': 'BELTRÁN',
    r'C\?RDENAS': 'CÁRDENAS', r'BRICE\?O': 'BRICEÑO', r'SULTOR\?A': 'SULTORÍA',
    r'M\?XICO': 'MÉXICO', r'CARRE\?O': 'CARREÑO', r'BORB\?N': 'BORBÓN',
    r'BARE\?O': 'BAREÑO', r'CABA\?AS': 'CABAÑAS', r'CEDE\?O': 'CEDEÑO',
    r'BURGUE\?O': 'BURGUEÑO', r'S\?NCHEZ': 'SÁNCHEZ', r'PE\?A': 'PEÑA',
    r'CAMPAÃ\?A': 'CAMPAÑA', r'MISI\?N': 'MISIÓN', r'DISE\?O': 'DISEÑO',
    r'GONZÃ\?LEZ': 'GONZÁLEZ', r'MUÃ\?OZ': 'MUÑOZ', r'YAÃ\?EZ': 'YAÑEZ',
    r'YA\?EZ': 'YAÑEZ', r'ZU\?IGA': 'ZUÑIGA', r'L\?PEZ': 'LÓPEZ',
    r'ELECTR\?N': 'ELECTRÓN', r'MAGA\?A': 'MAGAÑA', r'GOÃ\?I': 'GOÑI',
    r'IBA\?EZ': 'IBAÑEZ', r'FARMACÃ\?UTICA': 'FARMACÉUTICA', r'SE\?OR': 'SEÑOR',
    r'NU\?EZ': 'NUÑEZ', r'NUÃ\?EZ': 'NUÑEZ', r'PEÃ\?ON': 'PEÑÓN',
    r'PIÃ\?A': 'PIÑA', r'ORTU\?O': 'ORTUÑO', r'QUIÃ\?ONES': 'QUIÑONES',
    r'ENSEÃ\?ANZA': 'ENSEÑANZA', r'ESPAÃ\?': 'ESPAÑ', r'ESPA\?A': 'ESPAÑA',
    r'M\?LTIPLE': 'MÚLTIPLE', r'SAÃ\?UDO': 'SAÑUDO', r'TUR\?STIC': 'TURÍSTIC',
    r'MÃ\?XICO': 'MÉXICO', r'C\?SAR': 'CÉSAR', r'R\?OS': 'RÍOS',
    r'QUER\?TA': 'QUERÉTA',
    'Ã‘': 'Ñ', 'Ã±': 'ñ', 'Ã¡': 'á', 'Á ': 'á', 'Ã©': 'é', 'Ã‰': 'É',
    'Ã­': 'í', 'Ã\xad': 'í', 'Ã³': 'ó', 'Ã“': 'Ó', 'Ãº': 'ú', 'Ãš': 'Ú',
    'Ã¼': 'ü', 'Ãœ': 'Ü', 'Â¿': '¿', 'Â¡': '¡', 'Ã': 'Á', 'ÃA': 'ÍA',
    'UÃ': 'UÍ',
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
