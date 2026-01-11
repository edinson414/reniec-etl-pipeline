# ================================================================================
# FUNCIONES DE LIMPIEZA, DEDUPLICACIÓN Y GUARDADO DE EXCEL
# ================================================================================
import pandas as pd
import os
from openpyxl.styles import Font, PatternFill, Alignment
from config_archivos import (
    COLUMNAS_HISTORICO, 
    COLUMNAS_LIMPIO, 
    FORMATO_ENCABEZADO, 
    ANCHOS_COLUMNAS
)

def limpiar_y_deduplicar(df, modo='historico'):
    """
    Limpia el DataFrame y maneja la deduplicación según el modo.
    
    Args:
        df (pd.DataFrame): DataFrame a procesar
        modo (str): 'historico' (mantiene todos los periodos) o 'limpio' (solo últimos)
    
    Returns:
        pd.DataFrame: DataFrame procesado
    """
    df = df.fillna('')
    
    if modo == 'historico':
        # Deduplicación suave: solo elimina si es exactamente idéntica (incluyendo PERIODO)
        df_original = len(df)
        df = df.drop_duplicates()
        df_final = len(df)
        print(f"[DEDUP] Histórico: {df_original} -> {df_final} registros (eliminadas {df_original - df_final} filas idénticas)")
        
    elif modo == 'limpio':
        # Deduplicación agresiva: solo guarda la versión más reciente
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
    """
    Aplica formato visual al worksheet de Excel.
    
    Args:
        worksheet: Worksheet de openpyxl
        modo (str): 'historico' o 'limpio' (para saber qué columnas formatear)
    """
    # Encabezados con formato
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
    
    # Aplicar formato a encabezado
    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    # Ajustar ancho de columnas
    columnas = COLUMNAS_HISTORICO if modo == 'historico' else COLUMNAS_LIMPIO
    for i, col_name in enumerate(columnas, 1):
        col_letter = chr(64 + i)  # A, B, C, etc.
        ancho = ANCHOS_COLUMNAS.get(col_name, 20)
        worksheet.column_dimensions[col_letter].width = ancho
    
    # Configurar altura de encabezado
    worksheet.row_dimensions[1].height = FORMATO_ENCABEZADO['altura']

def guardar_excel(df, ruta_archivo, modo='historico'):
    """
    Guarda el DataFrame en formato Excel con formato aplicado.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar
        ruta_archivo (str): Ruta completa del archivo de salida
        modo (str): 'historico' o 'limpio'
    
    Returns:
        bool: True si fue exitoso, False si hay error
    """
    try:
        # Seleccionar columnas según el modo
        columnas = COLUMNAS_HISTORICO if modo == 'historico' else COLUMNAS_LIMPIO
        cols_exportar = [c for c in columnas if c in df.columns]
        df = df[cols_exportar]
        
        # Crear escritor de Excel
        with pd.ExcelWriter(ruta_archivo, engine='openpyxl') as writer:
            sheet_name = 'Historico' if modo == 'historico' else 'RENIEC'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Aplicar formato
            worksheet = writer.sheets[sheet_name]
            aplicar_formato_excel(worksheet, modo=modo)
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Guardando Excel: {e}")
        return False

def guardar_csv(df, ruta_archivo, modo='historico'):
    """
    Guarda el DataFrame en formato CSV como respaldo.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar
        ruta_archivo (str): Ruta completa del archivo de salida
        modo (str): 'historico' o 'limpio'
    
    Returns:
        bool: True si fue exitoso, False si hay error
    """
    try:
        # Seleccionar columnas según el modo
        columnas = COLUMNAS_HISTORICO if modo == 'historico' else COLUMNAS_LIMPIO
        cols_exportar = [c for c in columnas if c in df.columns]
        df = df[cols_exportar]
        
        df.to_csv(ruta_archivo, index=False, encoding='utf-8-sig')
        return True
        
    except Exception as e:
        print(f"[ERROR] Guardando CSV: {e}")
        return False

def mostrar_estadisticas(df_original, df_procesado, modo='historico'):
    """
    Muestra estadísticas del procesamiento.
    
    Args:
        df_original (pd.DataFrame): DataFrame antes de deduplicación
        df_procesado (pd.DataFrame): DataFrame después de deduplicación
        modo (str): 'historico' o 'limpio'
    """
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
