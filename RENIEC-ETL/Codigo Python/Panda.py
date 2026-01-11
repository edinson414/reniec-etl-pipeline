# ================================================================================
# PANDA.PY - EXTRACCIÓN Y CONSOLIDACIÓN DE DATOS RENIEC
# ================================================================================
# Script principal que orquesta todo el proceso
# ================================================================================

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Importar configuraciones y funciones
from config_paths import (
    RUTA_ORIGEN, 
    RUTA_DESTINO, 
    ARCHIVO_EXCEL_LIMPIO,
    ARCHIVO_EXCEL_HISTORICO,
    ARCHIVO_CSV_LIMPIO,
    ARCHIVO_CSV_HISTORICO
)
from procesamiento import leer_todos_archivos_csv
from limpieza_y_guardado import (
    limpiar_y_deduplicar, 
    guardar_excel, 
    guardar_csv,
    mostrar_estadisticas
)

# ================================================================================
# CONFIGURAR DIRECTORIO DE TRABAJO
# ================================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
os.chdir(parent_dir)

print(f"[INFO] Directorio de trabajo: {os.getcwd()}\n")

# ================================================================================
# FASE 1: LECTURA Y PROCESAMIENTO
# ================================================================================
print("="*80)
print("INICIANDO EXTRACCIÓN Y CONSOLIDACIÓN DE DATOS RENIEC")
print("="*80 + "\n")

# Leer todos los archivos CSV
df_consolidado = leer_todos_archivos_csv(RUTA_ORIGEN)

if len(df_consolidado) == 0:
    print("[ERROR] No se pudieron procesar los archivos CSV.")
    exit(1)

print(f"\n[RESUMEN] Total de registros leídos: {len(df_consolidado)}")

# ================================================================================
# FASE 2: GENERACIÓN DE VERSIÓN HISTÓRICA (CON TODOS LOS PERIODOS)
# ================================================================================
print("\n" + "="*80)
print("GENERANDO VERSIÓN HISTÓRICA COMPLETA")
print("="*80 + "\n")

df_historico = df_consolidado.copy()
df_historico_original = len(df_historico)

# Deduplicación suave (solo elimina filas idénticas)
df_historico = limpiar_y_deduplicar(df_historico, modo='historico')

# Mostrar estadísticas
mostrar_estadisticas(
    pd.DataFrame(index=range(df_historico_original)), 
    df_historico, 
    modo='historico'
)

# Guardar Excel histórico
print("[GUARDANDO] Versión Histórica...")
if guardar_excel(df_historico, ARCHIVO_EXCEL_HISTORICO, modo='historico'):
    print(f"[OK] {ARCHIVO_EXCEL_HISTORICO}")
# Guardar CSV histórico
if guardar_csv(df_historico, ARCHIVO_CSV_HISTORICO, modo='historico'):
    print(f"[OK] {ARCHIVO_CSV_HISTORICO}")
print(f"[DATOS] Registros en Histórico: {len(df_historico)}\n")

# ================================================================================
# FASE 3: GENERACIÓN DE VERSIÓN LIMPIA (SOLO LOCALES ÚNICOS)
# ================================================================================
print("="*80)
print("GENERANDO VERSIÓN LIMPIA (DIRECTORIO)")
print("="*80 + "\n")

df_limpio = df_consolidado.copy()
df_limpio_original = len(df_limpio)

# Deduplicación agresiva (mantiene solo la versión más reciente)
df_limpio = limpiar_y_deduplicar(df_limpio, modo='limpio')

# Mostrar estadísticas
mostrar_estadisticas(
    pd.DataFrame(index=range(df_limpio_original)), 
    df_limpio, 
    modo='limpio'
)

# Guardar Excel limpio
print("[GUARDANDO] Versión Limpia (Directorio)...")
if guardar_excel(df_limpio, ARCHIVO_EXCEL_LIMPIO, modo='limpio'):
    print(f"[OK] {ARCHIVO_EXCEL_LIMPIO}")
# Guardar CSV limpio
if guardar_csv(df_limpio, ARCHIVO_CSV_LIMPIO, modo='limpio'):
    print(f"[OK] {ARCHIVO_CSV_LIMPIO}")
print(f"[DATOS] Registros en Limpio: {len(df_limpio)}\n")

# ================================================================================
# RESUMEN FINAL
# ================================================================================
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