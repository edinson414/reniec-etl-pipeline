# ================================================================================
# CONFIG.PY - Configuración centralizada para el proyecto RENIEC-ETL
# ================================================================================
# Consolida config_paths.py, config_archivos.py y config_sql.py en un único módulo
# ================================================================================

import os
from pathlib import Path

# ================================================================================
# RUTAS DEL PROYECTO
# ================================================================================
PROJECT_DIR = Path(__file__).parent.parent  # Raíz del proyecto (analisis_reniec/)
DATA_DIR = PROJECT_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
DOCS_DIR = PROJECT_DIR / 'docs'
MODELS_DIR = PROJECT_DIR / 'models'
REPORTS_DIR = PROJECT_DIR / 'reports'

# Crear carpetas si no existen
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Archivos de entrada (CSV)
RUTA_ORIGEN = RAW_DATA_DIR

# Archivos de salida (Excel)
ARCHIVO_EXCEL_LIMPIO = PROCESSED_DATA_DIR / 'RENIEC_Datos_Consolidados_Limpios.xlsx'
ARCHIVO_EXCEL_HISTORICO = PROCESSED_DATA_DIR / 'RENIEC_Historico_Completo.xlsx'
ARCHIVO_CSV_LIMPIO = PROCESSED_DATA_DIR / 'RENIEC_Datos_Consolidados_Limpios.csv'
ARCHIVO_CSV_HISTORICO = PROCESSED_DATA_DIR / 'RENIEC_Historico_Completo.csv'

# ================================================================================
# CONFIGURACIÓN DE ARCHIVOS CSV - Separadores, filas a saltar y periodos
# ================================================================================
CONFIG_ARCHIVOS = {
    '1. Centros': {'sep': ';', 'skip': 0, 'periodo': '2021-01-01'}, 
    '2. Reporte Enero': {'sep': ',', 'skip': 0, 'periodo': '2021-12-31'},
    '3. Reporte I Semestre': {'sep': ',', 'skip': 0, 'periodo': '2022-06-30'},
    '4. Reporte III Trimestre 2022': {'sep': ',', 'skip': 0, 'periodo': '2022-09-30'},
    '5. Reporte IV': {'sep': ';', 'skip': 0, 'periodo': '2022-12-31'},
    '6. Reporte I Trimestre 2023': {'sep': ',', 'skip': 0, 'periodo': '2023-03-31'},
    '7. Reporte II Trimestre 2023': {'sep': ',', 'skip': 1, 'periodo': '2023-06-30'},
    '8. Reporte III Trimestre 2023': {'sep': ',', 'skip': 1, 'periodo': '2023-09-30'},
    '9. Reporte IV Trimestre 2023': {'sep': ',', 'skip': 1, 'periodo': '2023-12-31'},
    '10. Reporte I Trimestre 2024': {'sep': ',', 'skip': 1, 'periodo': '2024-03-31'},
    '11. Reporte II Trimestre 2024': {'sep': ',', 'skip': 1, 'periodo': '2024-06-30'},
    '12. Reporte III Trimestre 2024': {'sep': ',', 'skip': 0, 'periodo': '2024-09-30'},
    '13. Reporte IV Trimestre 2024': {'sep': ',', 'skip': 0, 'periodo': '2024-12-31'},
    '14. Reporte I Trimestre 2025': {'sep': ',', 'skip': 2, 'periodo': '2025-03-31'},
    '15. Reporte II Trimestre 2025': {'sep': ';', 'skip': 2, 'periodo': '2025-06-30'},
    '16. Reporte III Trimestre 2025': {'sep': ',', 'skip': 1, 'periodo': '2025-09-30'},
    '17. Reporte IV Trimestre 2025': {'sep': ';', 'skip': 1, 'periodo': '2025-12-31'},
}

# ================================================================================
# MAPEO DE COLUMNAS - Normalizar nombres para diferentes formatos
# ================================================================================
MAPA_COLUMNAS = {
    'CENTRO DE ATENCION': 'CENTRO DE ATENCION',
    'CENTRO DE ATENCIÓN': 'CENTRO DE ATENCION',
    'CENTRO DE ATENCIAN': 'CENTRO DE ATENCION',
    'NOMBRE LOCAL': 'CENTRO DE ATENCION',
    'DEPARTAMENTO': 'DEPARTAMENTO',
    'PROVINCIA': 'PROVINCIA',
    'DISTRITO': 'DISTRITO',
    'ESTADO': 'ESTADO',
    'ESTADO DE REINICIO DE OPERACIONES': 'ESTADO',
    'HORARIO DE ATENCIÓN AL PUBLICO': 'HORARIOS',
    'HORARIO DE ATENCION AL PUBLICO': 'HORARIOS',
    'HORARIO DE ATENCIAN AL PUBLICO': 'HORARIOS',
    'HORARIO DE ATENCIÓN': 'HORARIOS',
    'HORARIO DE ATENCION': 'HORARIOS',
    'HORARIO DE ATENCIAN': 'HORARIOS',
    'HORARIOS DE ATENCIÓN': 'HORARIOS',
    'HORARIOS DE ATENCION': 'HORARIOS',
    'HORARIOS DE ATENCIAN': 'HORARIOS',
    'NOMBRE DE LA VIA': 'DIRECCION',
    'DIRECCIÓN': 'DIRECCION',
    'DIRECCION': 'DIRECCION',
    'DIRECCIAN': 'DIRECCION',
    'ESTADO\nOPERATIVO: ATIENTE DE LUNES A VIERNES\nDEPLAZAMIENTO: ATIENDE DE ACUERDO A LA PROGRAMACION DE RENIEC': 'ESTADO',
}

# ================================================================================
# COLUMNAS ESTÁNDAR
# ================================================================================
COLUMNAS_DESEADAS = [
    'DEPARTAMENTO', 
    'PROVINCIA', 
    'DISTRITO', 
    'CENTRO DE ATENCION', 
    'ESTADO', 
    'HORARIOS', 
    'DIRECCION'
]

COLUMNAS_HISTORICO = [
    'PERIODO',
    'DEPARTAMENTO', 
    'PROVINCIA', 
    'DISTRITO', 
    'CENTRO DE ATENCION', 
    'ESTADO', 
    'HORARIOS', 
    'DIRECCION',
    'ARCHIVO_ORIGEN'
]

COLUMNAS_LIMPIO = [
    'PERIODO',
    'DEPARTAMENTO', 
    'PROVINCIA', 
    'DISTRITO', 
    'CENTRO DE ATENCION', 
    'ESTADO', 
    'HORARIOS', 
    'DIRECCION',
    'ARCHIVO_ORIGEN'
]

# ================================================================================
# CONFIGURACIÓN DE FORMATO EXCEL
# ================================================================================
FORMATO_ENCABEZADO = {
    'color_fondo': '366092',
    'color_texto': 'FFFFFF',
    'negrita': True,
    'tamaño': 11,
    'altura': 25
}

ANCHOS_COLUMNAS = {
    'PERIODO': 12,
    'DEPARTAMENTO': 20,
    'PROVINCIA': 20,
    'DISTRITO': 20,
    'CENTRO DE ATENCION': 35,
    'ESTADO': 30,
    'HORARIOS': 30,
    'DIRECCION': 40,
    'ARCHIVO_ORIGEN': 25
}

# ================================================================================
# CONFIGURACIÓN DE SQL SERVER
# ================================================================================
SQL_SERVER = 'EDINSON\\EDINSON'
SQL_DATABASE = 'DW_RENIEC_Gestion'
SQL_DRIVER = 'ODBC Driver 17 for SQL Server'
SQL_TRUSTED_CONNECTION = True
SQL_USERNAME = None
SQL_PASSWORD = None

TABLE_STAGING = 'TB_RENIEC_Historico_Stg'
TABLE_FINAL = 'TB_RENIEC_Historico'

SCHEMA_TABLA = {
    'PERIODO': 'DATE NOT NULL',
    'DEPARTAMENTO': 'VARCHAR(30)',
    'PROVINCIA': 'VARCHAR(30)',
    'DISTRITO': 'VARCHAR(30)',
    'CENTRO_ATENCION': 'VARCHAR(90)',
    'ESTADO': 'VARCHAR(100)',
    'HORARIOS': 'VARCHAR(150)',
    'DIRECCION': 'VARCHAR(150)',
    'ARCHIVO_ORIGEN': 'VARCHAR(100)'
}

INDICES = [
    ('IX_PERIODO', 'PERIODO'),
    ('IX_DEPARTAMENTO', 'DEPARTAMENTO'),
    ('IX_CENTRO_ATENCION', 'CENTRO_ATENCION'),
    ('IX_ESTADO', 'ESTADO')
]

BATCH_SIZE = 1000
TIMEOUT = 300
LOG_LEVEL = 'INFO'

print("[OK] Configuración cargada correctamente")
