# ================================================================================
# IMPORTAR_A_SQL_SERVER.PY - SCRIPT PRINCIPAL DE IMPORTACIÓN
# ================================================================================
# Orquesta todo el proceso de importación de datos a SQL Server
# ================================================================================

import sys
import os
from datetime import datetime

# Agregar ruta del script al PATH
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from config_sql import (
    SQL_SERVER, SQL_DATABASE, ARCHIVO_CSV_HISTORICO, 
    ARCHIVO_XLSX_HISTORICO, TABLE_STAGING, TABLE_FINAL
)
from conexion_sql import (
    crear_conexion, crear_tabla_staging, cargar_csv_a_sql,
    crear_tabla_final, transferir_staging_a_final, validar_carga,
    eliminar_tabla_staging, cerrar_conexion
)

# ================================================================================
# FUNCIÓN PRINCIPAL
# ================================================================================
def main():
    """Ejecuta el proceso completo de importación"""
    
    print("\n" + "="*80)
    print("IMPORTACIÓN DE DATOS RENIEC A SQL SERVER")
    print("="*80)
    print(f"\nServidor: {SQL_SERVER}")
    print(f"Base de Datos: {SQL_DATABASE}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    conn = None
    
    try:
        # Paso 1: Verificar que el archivo CSV existe
        print("[VERIFICACIÓN] Buscando archivo CSV...")
        if not os.path.exists(ARCHIVO_CSV_HISTORICO):
            print(f"[ERROR] No se encuentra: {ARCHIVO_CSV_HISTORICO}")
            return False
        print(f"[OK] {ARCHIVO_CSV_HISTORICO}")
        
        # Paso 2: Conectar a SQL Server
        print("\n[CONEXIÓN] Conectando a SQL Server...")
        conn = crear_conexion()
        
        # Paso 3: Crear tabla staging
        print("\n[CREACIÓN] Creando tabla staging...")
        crear_tabla_staging(conn)
        
        # Paso 4: Cargar datos desde CSV
        print("\n[CARGA] Importando datos desde CSV...")
        total_registros = cargar_csv_a_sql(conn, ARCHIVO_CSV_HISTORICO)
        
        # Paso 5: Crear tabla final
        print("\n[TABLA FINAL] Creando tabla final con índices...")
        crear_tabla_final(conn)
        
        # Paso 6: Transferir de staging a final
        print("\n[TRANSFERENCIA] Transfiriendo datos...")
        registros_finales = transferir_staging_a_final(conn)
        
        # Paso 7: Validar carga
        print("\n[VALIDACIÓN] Validando integridad de datos...")
        validar_carga(conn, ARCHIVO_CSV_HISTORICO)
        
        # Paso 8: Eliminar tabla staging (limpieza)
        print("\n[LIMPIEZA] Eliminando tabla staging...")
        eliminar_tabla_staging(conn)
        
        # Resumen final
        print("\n" + "="*80)
        print("[EXITO] PROCESO COMPLETADO EXITOSAMENTE")
        print("="*80)
        print(f"\nResumen:")
        print(f"  • Tabla Final: {TABLE_FINAL}")
        print(f"  • Registros Cargados: {registros_finales:,}")
        print(f"  • Servidor: {SQL_SERVER}")
        print(f"  • Base de Datos: {SQL_DATABASE}")
        print(f"  • Tabla Staging: Eliminada\n")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] El proceso falló: {e}\n")
        return False
        
    finally:
        if conn:
            cerrar_conexion(conn)

# ================================================================================
# EJECUTAR
# ================================================================================
if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
