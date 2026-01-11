# ================================================================================
# CONFIG_SQL.PY - CONFIGURACIÓN DE CONEXIÓN A SQL SERVER
# ================================================================================
# Parámetros de conexión y configuración de la base de datos
# ================================================================================

import os

# ================================================================================
# PARÁMETROS DE CONEXIÓN A SQL SERVER
# ================================================================================
SQL_SERVER = 'EDINSON\\EDINSON'      # Servidor SQL Server
SQL_DATABASE = 'DW_RENIEC_Gestion'   # Base de datos destino
SQL_DRIVER = 'ODBC Driver 17 for SQL Server'  # Driver ODBC
SQL_TRUSTED_CONNECTION = True         # Usar autenticación Windows (True/False)

# Si usas autenticación SQL (usuario/contraseña):
SQL_USERNAME = None  # ej: 'sa'
SQL_PASSWORD = None  # ej: 'password123'

# ================================================================================
# CONFIGURACIÓN DE TABLAS
# ================================================================================
TABLE_STAGING = 'TB_RENIEC_Historico_Stg'  # Tabla de carga temporal
TABLE_FINAL = 'TB_RENIEC_Historico'        # Tabla final con datos limpios

# ================================================================================
# RUTAS DE ARCHIVOS
# ================================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)  # Sube a la carpeta "2. RENIEC..."
PARENT_DIR = os.path.dirname(PARENT_DIR)  # Sube a carpeta de usuario
CSV_DIR = os.path.join(PARENT_DIR, '2. RENIEC - Centros de atención del RENIEC a nivel nacional [Registro Nacional de Identificación y Estado Civil]', 'CVS', 'Extraccion de los datos')
ARCHIVO_CSV_HISTORICO = os.path.join(CSV_DIR, 'RENIEC_Historico_Completo.csv')
ARCHIVO_XLSX_HISTORICO = os.path.join(CSV_DIR, 'RENIEC_Historico_Completo.xlsx')

# ================================================================================
# CONFIGURACIÓN DE CARGA
# ================================================================================
BATCH_SIZE = 1000          # Registros por lote
TIMEOUT = 300              # Timeout en segundos
LOG_LEVEL = 'INFO'         # DEBUG, INFO, WARNING, ERROR

# ================================================================================
# ESQUEMA DE TABLA
# ================================================================================
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

# ================================================================================
# ÍNDICES A CREAR
# ================================================================================
INDICES = [
    ('IX_PERIODO', 'PERIODO'),
    ('IX_DEPARTAMENTO', 'DEPARTAMENTO'),
    ('IX_CENTRO_ATENCION', 'CENTRO_ATENCION'),
    ('IX_ESTADO', 'ESTADO')
]

print("[OK] Configuración SQL Server cargada correctamente")
