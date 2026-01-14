"""
Carga el archivo limpio generado por la consolidación a SQL Server.

Ejecución recomendada (desde la carpeta del proyecto):
    python -m analisis_reniec.database.export_sql

Requiere haber ejecutado antes la consolidación para generar:
    data/processed/RENIEC_Datos_Consolidados_Limpios.csv
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd  # type: ignore
import pyodbc  # type: ignore

# Garantizar import correcto tanto si se ejecuta como módulo como si se lanza con F5
# PROJ_ROOT: carpeta raíz del proyecto (contiene el paquete analisis_reniec)
PROJ_ROOT = Path(__file__).resolve().parents[2]
PKG_ROOT = Path(__file__).resolve().parents[1]
for path in (PROJ_ROOT, PKG_ROOT):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from analisis_reniec.config import (  # noqa: E402
    PROCESSED_DATA_DIR,
    SQL_SERVER,
    SQL_DATABASE,
    SQL_DRIVER,
    SQL_TRUSTED_CONNECTION,
    SQL_USERNAME,
    SQL_PASSWORD,
    SCHEMA_TABLA,
    BATCH_SIZE,
    TIMEOUT,
)

TABLE_DESTINO = "TB_RENIEC_HISTORICO"
ARCHIVO_LIMPIO = PROCESSED_DATA_DIR / "RENIEC_Historico_Completo.csv"

COLUMN_MAP = {
    "PERIODO": "PERIODO",
    "DEPARTAMENTO": "DEPARTAMENTO",
    "PROVINCIA": "PROVINCIA",
    "DISTRITO": "DISTRITO",
    "CENTRO DE ATENCION": "CENTRO_ATENCION",
    "ESTADO": "ESTADO",
    "HORARIOS": "HORARIOS",
    "DIRECCION": "DIRECCION",
    "ARCHIVO_ORIGEN": "ARCHIVO_ORIGEN",
}


def obtener_conexion() -> pyodbc.Connection:
    """Crea la cadena de conexión a SQL Server."""
    if SQL_TRUSTED_CONNECTION:
        conn_str = (
            f"DRIVER={{{SQL_DRIVER}}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            "Trusted_Connection=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{{SQL_DRIVER}}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USERNAME};PWD={SQL_PASSWORD};"
        )
    return pyodbc.connect(conn_str, timeout=TIMEOUT)


def crear_tabla_si_no_existe(cursor: pyodbc.Cursor, tabla: str, esquema: Dict[str, str]) -> None:
    columnas = ", ".join([f"[{col}] {tipo}" for col, tipo in esquema.items()])
    sql = f"""
    IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE type = 'U' AND name = '{tabla}')
    BEGIN
        CREATE TABLE [{tabla}] (
            {columnas}
        );
    END
    """
    cursor.execute(sql)


def _normalize_name(name: str) -> str:
    return name.replace('\ufeff', '').strip().upper()


def preparar_dataframe() -> pd.DataFrame:
    if not ARCHIVO_LIMPIO.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo limpio en: {ARCHIVO_LIMPIO}. Ejecuta primero la consolidación."
        )

    df = pd.read_csv(ARCHIVO_LIMPIO, encoding='utf-8-sig')
    
    print(f"[DEBUG] Columnas originales del CSV: {list(df.columns)}")

    # Normalizar nombres y aplicar mapeo
    df.columns = [_normalize_name(c) for c in df.columns]
    df.rename(columns={_normalize_name(k): v for k, v in COLUMN_MAP.items()}, inplace=True)
    
    print(f"[DEBUG] Columnas después del mapeo: {list(df.columns)}")

    # Verificar columnas faltantes
    faltantes = [col for col in SCHEMA_TABLA.keys() if col not in df.columns]
    if faltantes:
        raise ValueError(
            f"Faltan columnas en el CSV: {faltantes}.\n"
            f"El CSV limpio debe tener PERIODO y ARCHIVO_ORIGEN.\n"
            f"Ejecuta primero: python -m analisis_reniec.main consolidar"
        )

    # Convertir PERIODO a fecha
    df["PERIODO"] = pd.to_datetime(df["PERIODO"], errors="coerce").dt.date
    
    # Reemplazar NaN con None para SQL Server
    df = df.where(pd.notna(df), None)
    
    return df[list(SCHEMA_TABLA.keys())]


def cargar_dataframe(cursor: pyodbc.Cursor, tabla: str, df: pd.DataFrame) -> None:
    cols = ",".join([f"[{col}]" for col in df.columns])
    placeholders = ",".join(["?"] * len(df.columns))
    insert_sql = f"INSERT INTO [{tabla}] ({cols}) VALUES ({placeholders})"

    datos: List[Tuple] = list(df.itertuples(index=False, name=None))
    for i in range(0, len(datos), BATCH_SIZE):
        batch = datos[i : i + BATCH_SIZE]
        cursor.fast_executemany = True
        cursor.executemany(insert_sql, batch)


def main() -> None:
    print("\n=== CARGA DE ARCHIVO LIMPIO A SQL SERVER ===\n")
    df = preparar_dataframe()
    print(f"[OK] DataFrame preparado: {len(df)} filas")

    with obtener_conexion() as conn:
        cursor = conn.cursor()
        print(f"[OK] Conectado a SQL Server: {SQL_SERVER} / BD: {SQL_DATABASE}")
        crear_tabla_si_no_existe(cursor, TABLE_DESTINO, SCHEMA_TABLA)
        print(f"[OK] Tabla verificada/creada: {TABLE_DESTINO}")
        cargar_dataframe(cursor, TABLE_DESTINO, df)
        conn.commit()
        print(f"[OK] Filas insertadas: {len(df)}")

    print("\n[EXITO] Carga completada. Tabla destino:", TABLE_DESTINO)


if __name__ == "__main__":
    main()
