# ================================================================================
# CONFIGURACIÓN DE ARCHIVOS Y MAPEO DE COLUMNAS
# ================================================================================

# ================================================================================
# CONFIGURACIÓN DE ARCHIVOS - Separadores, filas a saltar y periodos
# ================================================================================
# Con PERIODO asignado para mantener histórico
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
# COLUMNAS ESTÁNDAR REQUERIDAS
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

# Orden final de columnas en Excel (HISTÓRICO)
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

# Orden final de columnas en Excel (LIMPIO)
COLUMNAS_LIMPIO = [
    'DEPARTAMENTO', 
    'PROVINCIA', 
    'DISTRITO', 
    'CENTRO DE ATENCION', 
    'ESTADO', 
    'HORARIOS', 
    'DIRECCION'
]

# ================================================================================
# CONFIGURACIÓN DE FORMATO EXCEL
# ================================================================================
FORMATO_ENCABEZADO = {
    'color_fondo': '366092',  # Azul oscuro
    'color_texto': 'FFFFFF',  # Blanco
    'negrita': True,
    'tamaño': 11,
    'altura': 30
}

ANCHOS_COLUMNAS = {
    'PERIODO': 15,
    'DEPARTAMENTO': 30,
    'PROVINCIA': 30,
    'DISTRITO': 30,
    'CENTRO DE ATENCION': 90,
    'ESTADO': 20,
    'HORARIOS': 50,
    'DIRECCION': 150,
    'ARCHIVO_ORIGEN': 40
}
