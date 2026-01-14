# ================================================================================
# FEATURES.PY - Limpieza, deduplicación y guardado de datos
# ================================================================================
# Refactorizado de: limpieza_y_guardado.py
# ================================================================================

import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from analisis_reniec.config import (
    COLUMNAS_HISTORICO, 
    COLUMNAS_LIMPIO, 
    FORMATO_ENCABEZADO, 
    ANCHOS_COLUMNAS
)

def limpiar_y_deduplicar(df, modo='historico'):
    """Limpia el DataFrame y maneja la deduplicación según el modo."""
    df = df.fillna('')
    
    if modo == 'historico':
        df_original = len(df)
        df = df.drop_duplicates()
        df_final = len(df)
        print(f"[DEDUP] Histórico: {df_original} -> {df_final} registros (eliminadas {df_original - df_final} filas idénticas)")
        
    elif modo == 'limpio':
        df_original = len(df)
        df = df.sort_values('PERIODO', ascending=False)
        df = df.drop_duplicates(
            subset=['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'CENTRO DE ATENCION'],
            keep='first'
        )
        df_final = len(df)
        duplicados = df_original - df_final
        print(f"[DEDUP] Limpio: {df_original} registros -> {df_final} únicos (eliminados {duplicados} duplicados históricos)")
    
    return df

def aplicar_formato_excel(worksheet, modo='historico'):
    """Aplica formato visual al worksheet de Excel."""
    header_fill = PatternFill(
        start_color=FORMATO_ENCABEZADO['color_fondo'], 
        end_color=FORMATO_ENCABEZADO['color_fondo'], 
        fill_type='solid'
    )
    header_font = Font(
        bold=FORMATO_ENCABEZADO['negrita'], 
        color=FORMATO_ENCABEZADO['color_texto'], 
        size=FORMATO_ENCABEZADO['tamaño']
    )
    
    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    columnas = COLUMNAS_HISTORICO if modo == 'historico' else COLUMNAS_LIMPIO
    for i, col_name in enumerate(columnas, 1):
        col_letter = chr(64 + i)
        ancho = ANCHOS_COLUMNAS.get(col_name, 20)
        worksheet.column_dimensions[col_letter].width = ancho
    
    worksheet.row_dimensions[1].height = FORMATO_ENCABEZADO['altura']

def guardar_excel(df, ruta_archivo, modo='historico'):
    """Guarda el DataFrame en formato Excel con formato aplicado."""
    try:
        columnas = COLUMNAS_HISTORICO if modo == 'historico' else COLUMNAS_LIMPIO
        cols_exportar = [c for c in columnas if c in df.columns]
        df = df[cols_exportar]
        
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            sheet_name = 'Historico' if modo == 'historico' else 'RENIEC'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            worksheet = writer.sheets[sheet_name]
            aplicar_formato_excel(worksheet, modo=modo)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Guardando Excel: {e}")
        return False

def guardar_csv(df, ruta_archivo, modo='historico'):
    """Guarda el DataFrame en formato CSV como respaldo."""
    try:
        columnas = COLUMNAS_HISTORICO if modo == 'historico' else COLUMNAS_LIMPIO
        cols_exportar = [c for c in columnas if c in df.columns]
        df = df[cols_exportar]
        df.to_csv(ruta_archivo, index=False, encoding='utf-8-sig')
        return True
        
    except Exception as e:
        print(f"[ERROR] Guardando CSV: {e}")
        return False

def mostrar_estadisticas(df_original, df_procesado, modo='historico'):
    """Muestra estadísticas del procesamiento."""
    print("\n" + "="*80)
    print(f"ESTADÍSTICAS DE PROCESAMIENTO ({modo.upper()})")
    print("="*80)
    print(f"[DATOS] Registros antes de limpieza: {len(df_original)}")
    print(f"[DATOS] Registros después de limpieza: {len(df_procesado)}")
    print(f"[DATOS] Registros eliminados: {len(df_original) - len(df_procesado)}")
    if len(df_original) > 0:
        porcentaje = (len(df_procesado) / len(df_original)) * 100
        print(f"[DATOS] Retención: {porcentaje:.1f}%")
    print("="*80 + "\n")
