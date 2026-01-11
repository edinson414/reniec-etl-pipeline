# ================================================================================
# CONFIGURACIÓN DE RUTAS
# ================================================================================
import os

# Obtener el directorio del script y el directorio padre
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

# Rutas principales
RUTA_ORIGEN = os.path.join(parent_dir, 'CVS')
RUTA_DESTINO = os.path.join(RUTA_ORIGEN, 'Extraccion de los datos')

# Archivos de salida
ARCHIVO_EXCEL_LIMPIO = os.path.join(RUTA_DESTINO, 'RENIEC_Datos_Consolidados_Limpios.xlsx')
ARCHIVO_EXCEL_HISTORICO = os.path.join(RUTA_DESTINO, 'RENIEC_Historico_Completo.xlsx')
ARCHIVO_CSV_LIMPIO = os.path.join(RUTA_DESTINO, 'RENIEC_Datos_Consolidados_Limpios.csv')
ARCHIVO_CSV_HISTORICO = os.path.join(RUTA_DESTINO, 'RENIEC_Historico_Completo.csv')

# Crear carpeta de destino si no existe
if not os.path.exists(RUTA_DESTINO):
    os.makedirs(RUTA_DESTINO)
    print(f"[OK] Carpeta creada: {RUTA_DESTINO}")
