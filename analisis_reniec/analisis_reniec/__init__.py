"""
Proyecto RENIEC-ETL: Consolidación y análisis de datos de centros de atención del RENIEC

Este paquete contiene módulos para:
- Lectura y procesamiento de archivos CSV
- Consolidación y limpieza de datos
- Exportación a Excel con formato profesional
- Carga de datos a SQL Server
"""

__version__ = "1.0.0"
__author__ = "Análisis de Datos"

from .config import (
    PROJECT_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
)

__all__ = [
    "PROJECT_DIR",
    "DATA_DIR",
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
]
