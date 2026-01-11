# ================================================================================
# CONEXION_SQL.PY - GESTIÓN DE CONEXIÓN A SQL SERVER
# ================================================================================
# Funciones para conectar y ejecutar operaciones en SQL Server
# ================================================================================

import pyodbc
import pandas as pd
import logging
from datetime import datetime
from config_sql import (
    SQL_SERVER, SQL_DATABASE, SQL_DRIVER, SQL_USERNAME, SQL_PASSWORD,
    SQL_TRUSTED_CONNECTION, ARCHIVO_CSV_HISTORICO,
    TABLE_STAGING, TABLE_FINAL, SCHEMA_TABLA, INDICES, TIMEOUT
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# ================================================================================
# CREAR CONEXIÓN A SQL SERVER
# ================================================================================
def crear_conexion():
    """Crea conexión a SQL Server"""
    try:
        if SQL_TRUSTED_CONNECTION:
            # Autenticación Windows
            connection_string = (
                f'Driver={{{SQL_DRIVER}}};'
                f'Server={SQL_SERVER};'
                f'Database={SQL_DATABASE};'
                f'Trusted_Connection=yes;'
            )
        else:
            # Autenticación SQL Server
            connection_string = (
                f'Driver={{{SQL_DRIVER}}};'
                f'Server={SQL_SERVER};'
                f'Database={SQL_DATABASE};'
                f'UID={SQL_USERNAME};'
                f'PWD={SQL_PASSWORD};'
            )
        
        conn = pyodbc.connect(connection_string, timeout=TIMEOUT)
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        logger.info(f"[OK] Conectado a {SQL_SERVER}.{SQL_DATABASE}")
        return conn
    except pyodbc.Error as e:
        logger.error(f"[ERROR] No se pudo conectar a SQL Server: {e}")
        raise

# ================================================================================
# CREAR TABLA STAGING
# ================================================================================
def crear_tabla_staging(conn):
    """Crea tabla staging para carga de datos"""
    cursor = conn.cursor()
    try:
        # Verificar si la tabla existe
        cursor.execute(f"""
            IF OBJECT_ID('{TABLE_STAGING}', 'U') IS NOT NULL
            DROP TABLE {TABLE_STAGING}
        """)
        conn.commit()
        logger.info(f"[OK] Tabla {TABLE_STAGING} eliminada si existía")
        
        # Crear tabla
        columnas = []
        for col, tipo in SCHEMA_TABLA.items():
            columnas.append(f"{col} {tipo}")
        
        sql_create = f"""
            CREATE TABLE {TABLE_STAGING} (
                {', '.join(columnas)}
            )
        """
        
        cursor.execute(sql_create)
        conn.commit()
        logger.info(f"[OK] Tabla {TABLE_STAGING} creada exitosamente")
        
    except pyodbc.Error as e:
        logger.error(f"[ERROR] No se pudo crear tabla staging: {e}")
        raise
    finally:
        cursor.close()

# ================================================================================
# CARGAR DATOS DESDE CSV
# ================================================================================
def cargar_csv_a_sql(conn, archivo_csv, batch_size=1000):
    """Carga datos desde CSV a tabla staging"""
    try:
        logger.info(f"[LEYENDO] {archivo_csv}")
        df = pd.read_csv(archivo_csv, encoding='utf-8-sig')
        
        # Renombrar columnas para coincidir con el esquema SQL
        if 'CENTRO DE ATENCION' in df.columns:
            df = df.rename(columns={'CENTRO DE ATENCION': 'CENTRO_ATENCION'})
        
        # Remover FECHA_CARGA si existe (SQL Server la genera automáticamente)
        if 'FECHA_CARGA' in df.columns:
            df = df.drop(columns=['FECHA_CARGA'])
        
        # Limpiar valores NaN
        df = df.fillna('')
        
        # Convertir PERIODO a formato DATE si existe
        if 'PERIODO' in df.columns:
            df['PERIODO'] = pd.to_datetime(df['PERIODO'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        logger.info(f"[OK] {len(df)} registros leídos")
        
        cursor = conn.cursor()
        cursor.fast_executemany = True  # Modo rápido para inserción masiva
        
        # Insertar en lotes
        total = len(df)
        columnas = list(SCHEMA_TABLA.keys())
        placeholders = ','.join(['?' for _ in columnas])
        columnas_str = ','.join(columnas)
        
        sql_insert = f"""
            INSERT INTO {TABLE_STAGING} ({columnas_str})
            VALUES ({placeholders})
        """
        
        for i in range(0, total, batch_size):
            lote = df.iloc[i:i+batch_size]
            
            # Convertir fila a tupla para ejecutemany
            valores_lote = []
            for _, row in lote.iterrows():
                valores = tuple(
                    None if pd.isna(row.get(col)) or row.get(col) == '' else str(row.get(col)).strip()
                    for col in columnas
                )
                valores_lote.append(valores)
            
            # Insertar lote completo
            try:
                cursor.executemany(sql_insert, valores_lote)
                conn.commit()
                logger.info(f"[PROGRESO] {min(i+batch_size, total)}/{total} registros insertados")
            except Exception as batch_error:
                logger.error(f"[ADVERTENCIA] Error en lote {i//batch_size + 1}: {batch_error}")
                # Insertar fila por fila para identificar problema
                for valores in valores_lote:
                    try:
                        cursor.execute(sql_insert, valores)
                        conn.commit()
                    except Exception as row_error:
                        logger.error(f"[ERROR] Fila problemática: {valores} - {row_error}")
        
        logger.info(f"[EXITO] {total} registros cargados en {TABLE_STAGING}")
        return total
        
    except Exception as e:
        logger.error(f"[ERROR] No se pudo cargar CSV: {e}")
        raise
    finally:
        cursor.close()

# ================================================================================
# CREAR TABLA FINAL
# ================================================================================
def crear_tabla_final(conn):
    """Crea tabla final a partir de staging"""
    cursor = conn.cursor()
    try:
        # Verificar si existe
        cursor.execute(f"""
            IF OBJECT_ID('{TABLE_FINAL}', 'U') IS NOT NULL
            DROP TABLE {TABLE_FINAL}
        """)
        conn.commit()
        logger.info(f"[OK] Tabla {TABLE_FINAL} eliminada si existía")
        
        # Crear tabla final con índices
        columnas = []
        for col, tipo in SCHEMA_TABLA.items():
            columnas.append(f"{col} {tipo}")
        
        sql_create = f"""
            CREATE TABLE {TABLE_FINAL} (
                ID INT IDENTITY(1,1) PRIMARY KEY,
                {', '.join(columnas)}
            )
        """
        
        cursor.execute(sql_create)
        conn.commit()
        logger.info(f"[OK] Tabla {TABLE_FINAL} creada")
        
        # Crear índices
        for nombre_idx, columna in INDICES:
            try:
                cursor.execute(f"""
                    CREATE INDEX {nombre_idx}
                    ON {TABLE_FINAL} ({columna})
                """)
                conn.commit()
                logger.info(f"[OK] Índice {nombre_idx} creado")
            except:
                pass
        
    except pyodbc.Error as e:
        logger.error(f"[ERROR] No se pudo crear tabla final: {e}")
        raise
    finally:
        cursor.close()

# ================================================================================
# TRANSFERIR DE STAGING A FINAL
# ================================================================================
def transferir_staging_a_final(conn):
    """Transfiere datos de staging a tabla final"""
    cursor = conn.cursor()
    try:
        columnas = ','.join(SCHEMA_TABLA.keys())
        
        sql_insert = f"""
            INSERT INTO {TABLE_FINAL} ({columnas})
            SELECT {columnas} FROM {TABLE_STAGING}
        """
        
        cursor.execute(sql_insert)
        conn.commit()
        
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_FINAL}")
        total = cursor.fetchone()[0]
        
        logger.info(f"[OK] {total} registros transferidos a {TABLE_FINAL}")
        return total
        
    except pyodbc.Error as e:
        logger.error(f"[ERROR] No se pudo transferir datos: {e}")
        raise
    finally:
        cursor.close()

# ================================================================================
# VALIDAR DATOS
# ================================================================================
def validar_carga(conn, archivo_csv):
    """Valida que los datos se cargaron correctamente"""
    try:
        df = pd.read_csv(archivo_csv, encoding='utf-8-sig')
        registros_csv = len(df)
        
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_FINAL}")
        registros_sql = cursor.fetchone()[0]
        cursor.close()
        
        logger.info(f"[VALIDACIÓN]")
        logger.info(f"  Registros en CSV: {registros_csv}")
        logger.info(f"  Registros en SQL: {registros_sql}")
        
        if registros_csv == registros_sql:
            logger.info(f"[OK] Validación exitosa")
            return True
        else:
            logger.warning(f"[ADVERTENCIA] Discrepancia en registros")
            return False
            
    except Exception as e:
        logger.error(f"[ERROR] No se pudo validar: {e}")
        return False

# ================================================================================
# ELIMINAR TABLA STAGING
# ================================================================================
def eliminar_tabla_staging(conn):
    """Elimina tabla staging después de transferencia"""
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            IF OBJECT_ID('{TABLE_STAGING}', 'U') IS NOT NULL
            DROP TABLE {TABLE_STAGING}
        """)
        conn.commit()
        logger.info(f"[OK] Tabla {TABLE_STAGING} eliminada exitosamente")
    except pyodbc.Error as e:
        logger.error(f"[ERROR] No se pudo eliminar tabla staging: {e}")
        raise
    finally:
        cursor.close()

# ================================================================================
# CERRAR CONEXIÓN
# ================================================================================
def cerrar_conexion(conn):
    """Cierra conexión a SQL Server"""
    try:
        conn.close()
        logger.info("[OK] Conexión cerrada")
    except Exception as e:
        logger.error(f"[ERROR] No se pudo cerrar conexión: {e}")
