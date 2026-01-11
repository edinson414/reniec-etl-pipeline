# ================================================================================
# FUNCIONES DE LECTURA Y PROCESAMIENTO DE ARCHIVOS CSV
# ================================================================================
import pandas as pd
import os
from config_archivos import CONFIG_ARCHIVOS, MAPA_COLUMNAS, COLUMNAS_DESEADAS

def limpiar_nombres_columnas(df):
    """
    Limpia y normaliza los nombres de las columnas.
    Elimina BOM, espacios en blanco, caracteres especiales.
    """
    # Eliminar BOM si existe
    df.columns = df.columns.str.replace('\ufeff', '', regex=False)
    df.columns = df.columns.str.replace('ï»¿', '', regex=False)
    
    # Eliminar espacios y convertir a mayúsculas
    df.columns = df.columns.str.strip().str.upper()
    
    # Normalizar caracteres especiales
    df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    
    return df

def limpiar_valores_columnas(df):
    """
    Limpia espacios en blanco en valores de texto.
    Elimina filas completamente vacías.
    """
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
    
    # Eliminar filas completamente vacías
    df = df.dropna(how='all')
    
    return df

def mapear_columnas(df):
    """
    Aplica el mapeo de columnas usando el diccionario MAPA_COLUMNAS.
    """
    df.rename(columns=MAPA_COLUMNAS, inplace=True)
    return df

def seleccionar_columnas_necesarias(df, nombre_archivo):
    """
    Selecciona solo las columnas deseadas.
    Retorna las columnas disponibles y emite advertencias si faltan.
    """
    cols_disponibles = [c for c in COLUMNAS_DESEADAS if c in df.columns]
    
    if len(cols_disponibles) < 4:
        print(f"      [ADVERTENCIA] Columnas esperadas encontradas: {cols_disponibles}")
        todas_cols = list(df.columns)[:20]
        print(f"      [INFO] Columnas disponibles (primeras 20): {todas_cols}")
    
    if len(cols_disponibles) > 0:
        return df[cols_disponibles]
    else:
        print(f"      [ERROR] No se encontraron columnas esperadas")
        return None

def procesar_archivo_csv(archivo_path, nombre_archivo):
    """
    Lee y procesa un archivo CSV completo.
    
    Args:
        archivo_path (str): Ruta completa del archivo
        nombre_archivo (str): Nombre del archivo
    
    Returns:
        pd.DataFrame: DataFrame procesado o None si hay error
    """
    # Buscar configuración del archivo
    conf = {'sep': ',', 'skip': 0, 'periodo': 'DESCONOCIDO'}
    for clave, valores in CONFIG_ARCHIVOS.items():
        if clave in nombre_archivo:
            conf = valores
            break
    
    try:
        print(f"[LEY] Leyendo: {nombre_archivo}")
        
        # Leer CSV con manejo de errores
        df = pd.read_csv(
            archivo_path, 
            sep=conf['sep'], 
            skiprows=conf['skip'], 
            encoding='latin-1', 
            on_bad_lines='skip'
        )
        
        print(f"      Columnas encontradas: {len(df.columns)}")
        if len(df.columns) <= 10:
            print(f"      Nombres: {list(df.columns)}")
        
        # Aplicar limpieza y procesamiento
        df = limpiar_nombres_columnas(df)
        df = mapear_columnas(df)
        df = seleccionar_columnas_necesarias(df, nombre_archivo)
        
        if df is None:
            return None
        
        df = limpiar_valores_columnas(df)
        
        # Agregar metadatos
        df['PERIODO'] = conf['periodo']
        df['ARCHIVO_ORIGEN'] = nombre_archivo
        
        print(f"      [OK] Procesado: {len(df)} registros (Período: {conf['periodo']})\n")
        
        return df
        
    except Exception as e:
        print(f"      [ERROR] {str(e)}\n")
        return None

def leer_todos_archivos_csv(ruta_origen):
    """
    Lee y procesa todos los archivos CSV de la carpeta.
    
    Args:
        ruta_origen (str): Ruta a la carpeta con archivos CSV
    
    Returns:
        pd.DataFrame: DataFrame consolidado con todos los archivos
    """
    df_final = pd.DataFrame()
    archivos_csv = [f for f in os.listdir(ruta_origen) if f.endswith('.csv')]
    archivos_encontrados = sorted([os.path.join(ruta_origen, f) for f in archivos_csv])
    
    print(f"[INFO] Archivos CSV encontrados: {len(archivos_encontrados)}\n")
    
    for archivo_path in archivos_encontrados:
        nombre_archivo = os.path.basename(archivo_path)
        df = procesar_archivo_csv(archivo_path, nombre_archivo)
        
        if df is not None and len(df) > 0:
            df_final = pd.concat([df_final, df], ignore_index=True)
    
    return df_final
