# ================================================================================
# PIPELINE.PY - Pipeline de consolidación de datos
# ================================================================================
# Refactorizado de: Panda.py
# ================================================================================

import pandas as pd
import os
import warnings
import sys

warnings.filterwarnings('ignore')

# Agregar carpeta padre al PATH para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analisis_reniec.config import (
    RUTA_ORIGEN, 
    ARCHIVO_EXCEL_LIMPIO,
    ARCHIVO_EXCEL_HISTORICO,
    ARCHIVO_CSV_LIMPIO,
    ARCHIVO_CSV_HISTORICO
)
from analisis_reniec.dataset import leer_todos_archivos_csv
from analisis_reniec.features import (
    limpiar_y_deduplicar, 
    guardar_excel, 
    guardar_csv,
    mostrar_estadisticas
)

def ejecutar_consolidacion():
    """Ejecuta el proceso completo de consolidación de datos."""
    
    print("\n" + "="*80)
    print("INICIANDO EXTRACCIÓN Y CONSOLIDACIÓN DE DATOS RENIEC")
    print("="*80 + "\n")

    # Fase 1: Lectura y procesamiento
    print("="*80)
    print("FASE 1: LECTURA Y PROCESAMIENTO")
    print("="*80 + "\n")
    
    df_consolidado = leer_todos_archivos_csv(RUTA_ORIGEN)

    if len(df_consolidado) == 0:
        print("[ERROR] No se pudieron procesar los archivos CSV.")
        return False

    print(f"\n[RESUMEN] Total de registros leídos: {len(df_consolidado)}")

    # Fase 2: Generación del archivo histórico
    print("\n" + "="*80)
    print("FASE 2: GENERANDO VERSIÓN HISTÓRICA COMPLETA")
    print("="*80 + "\n")

    df_historico = df_consolidado.copy()
    df_historico_original = len(df_historico)

    df_historico = limpiar_y_deduplicar(df_historico, modo='historico')

    mostrar_estadisticas(
        pd.DataFrame(index=range(df_historico_original)), 
        df_historico, 
        modo='historico'
    )

    print("[GUARDANDO] Versión Histórica...")
    if guardar_excel(df_historico, str(ARCHIVO_EXCEL_HISTORICO), modo='historico'):
        print(f"[OK] {ARCHIVO_EXCEL_HISTORICO}")
    if guardar_csv(df_historico, str(ARCHIVO_CSV_HISTORICO), modo='historico'):
        print(f"[OK] {ARCHIVO_CSV_HISTORICO}")
    print(f"[DATOS] Registros en Histórico: {len(df_historico)}\n")

    # Fase 3: Generación del archivo limpio
    print("="*80)
    print("FASE 3: GENERANDO VERSIÓN LIMPIA (DIRECTORIO)")
    print("="*80 + "\n")

    df_limpio = df_consolidado.copy()
    df_limpio_original = len(df_limpio)

    df_limpio = limpiar_y_deduplicar(df_limpio, modo='limpio')

    mostrar_estadisticas(
        pd.DataFrame(index=range(df_limpio_original)), 
        df_limpio, 
        modo='limpio'
    )

    print("[GUARDANDO] Versión Limpia (Directorio)...")
    if guardar_excel(df_limpio, str(ARCHIVO_EXCEL_LIMPIO), modo='limpio'):
        print(f"[OK] {ARCHIVO_EXCEL_LIMPIO}")
    if guardar_csv(df_limpio, str(ARCHIVO_CSV_LIMPIO), modo='limpio'):
        print(f"[OK] {ARCHIVO_CSV_LIMPIO}")
    print(f"[DATOS] Registros en Limpio: {len(df_limpio)}\n")

    # Resumen final
    print("="*80)
    print("[EXITO] PROCESO COMPLETADO")
    print("="*80)
    print("\n[ARCHIVOS GENERADOS]")
    print(f"  1. Histórico:  {len(df_historico):,} registros")
    print(f"     └─ {ARCHIVO_EXCEL_HISTORICO}")
    print(f"\n  2. Limpio:     {len(df_limpio):,} registros únicos")
    print(f"     └─ {ARCHIVO_EXCEL_LIMPIO}")
    print("\n[INFORMACIÓN]")
    print(f"  • Usa el archivo HISTÓRICO para análisis de tendencias (Power BI)")
    print(f"  • Usa el archivo LIMPIO para un directorio telefónico actualizado")
    print("\n")
    
    return True

if __name__ == '__main__':
    success = ejecutar_consolidacion()
    exit(0 if success else 1)
