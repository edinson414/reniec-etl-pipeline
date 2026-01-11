# RENIEC - Sistema de Extraccion y Consolidacion de Datos

## Documentacion Completa del Procesamiento Pandas

**Versión:** 2.0 (Modular)
**Última actualización:** 11 de Enero de 2026
**Estado:** Funcional y Optimizado

---

## Tabla de Contenidos

1. Estructura de Archivos
2. Descripción de Módulos
3. Flujo del Proceso
4. ¿Cuál archivo usar?
5. Cómo usar el sistema
6. Personalización
7. Troubleshooting
8. Próximos Pasos

---

## Estructura de Archivos

`text
Codigo Python/

- Panda.py (SCRIPT PRINCIPAL)
- config_paths.py (Configuración de rutas)
- config_archivos.py (Configuración de archivos)
- procesamiento.py (Lectura y procesamiento)
- limpieza_y_guardado.py (Deduplicación y guardado)
- documentacion_pandas.md (Documentación)
- .venv/ (Virtual environment)
`text

---

## Descripción de Módulos

### 1. Panda.py - Script Principal

**Propósito:** Coordina todo el flujo de extracción y consolidación

**Lo que hace:**

- Lee todas las configuraciones de los módulos
- Ejecuta el procesamiento de los 17 archivos CSV
- Genera 2 versiones del Excel (histórica + limpia)
- Muestra estadísticas del procesamiento
- Maneja errores y genera respaldos en CSV

**Líneas de código:** 95 (muy limpio)

**Para ejecutar:**

`text
python Panda.py
`text

**Salida esperada:**

`text
INICIANDO EXTRACCIÓN Y CONSOLIDACIÓN DE DATOS RENIEC
PROCESO COMPLETADO EXITOSAMENTE
Histórico: 7,752 registros
Limpio: 1,027 registros únicos
`text

---

### 2. config_paths.py - Configuración de Rutas

**Propósito:** Centralizar todas las rutas del proyecto

**Contenido:**

- RUTA_ORIGEN: Donde están los CSV
- RUTA_DESTINO: Donde guardar Excel
- ARCHIVO_EXCEL_LIMPIO: Ruta del Excel
- ARCHIVO_EXCEL_HISTORICO: Ruta del Excel histórico

**Ventaja:**

- Si cambias ubicación de carpetas, editas SOLO este archivo
- No necesitas tocar Panda.py

**Cuándo editar:**

- Si RENIEC te da los archivos en otra carpeta
- Si necesitas guardar en otra ubicación

---

### 3. config_archivos.py - Configuración de Datos

**Propósito:** Define como procesar cada CSV y mapear columnas

**Secciones principales:**

#### A) CONFIG_ARCHIVOS - Configuración por archivo

`text
'1. Centros': {
    'sep': ';',
    'skip': 0,
    'periodo': '2021-01-01'
}
`text

#### B) MAPA_COLUMNAS - Normalización de nombres

`text
'CENTRO DE ATENCIÓN': 'CENTRO DE ATENCION'
'NOMBRE LOCAL': 'CENTRO DE ATENCION'
`text

**Razón del mapeo:**

Cada reporte CSV tiene nombres diferentes:

- Reporte 2021: CENTRO DE ATENCIÓN
- Reporte 2023: NOMBRE LOCAL
- Reporte 2024: CENTRO DE ATENCION

Todas se mapean a CENTRO DE ATENCION

#### C) Otras configuraciones

- COLUMNAS_DESEADAS: Los 7 campos estándar
- COLUMNAS_HISTORICO: Orden en Excel histórico
- COLUMNAS_LIMPIO: Orden en Excel limpio
- FORMATO_ENCABEZADO: Color azul, blanco, negrita
- ANCHOS_COLUMNAS: Ancho de cada columna

**Cuándo editar:**

- Nuevo CSV de RENIEC: agrega 1 línea
- Nombre de columna: actualiza MAPA_COLUMNAS
- Otro color: modifica FORMATO_ENCABEZADO

---

### 4. procesamiento.py - Lectura y Procesamiento

**Propósito:** Funciones para leer y limpiar datos de CSV

**Funciones principales:**

- limpiar_nombres_columnas(): Elimina BOM
- limpiar_valores_columnas(): Limpia espacios
- mapear_columnas(): Aplica mapeo
- seleccionar_columnas_necesarias(): Extrae 7 columnas
- procesar_archivo_csv(): Procesa UN archivo
- leer_todos_archivos_csv(): Procesa todos los 17

**Ventaja:** Las funciones son reutilizables

---

### 5. limpieza_y_guardado.py - Deduplicación y Excel

**Propósito:** Funciones finales para guardar en Excel

**Funciones principales:**

- limpiar_y_deduplicar(): Modo histórico o limpio
- aplicar_formato_excel(): Aplica formato visual
- guardar_excel(): Guarda en Excel
- guardar_csv(): Guarda respaldo en CSV
- mostrar_estadisticas(): Imprime resultados

**Diferencia entre modos:**

HISTÓRICO (7,752 registros):

- Mantiene todos los períodos
- Puedes ver cambios en el tiempo

LIMPIO (1,027 registros):

- Solo la versión más reciente
- Funciona como directorio

---

## Flujo del Proceso

`text
python Panda.py
    ↓
FASE 1: LECTURA Y PROCESAMIENTO

- Busca 17 archivos CSV
- Limpia nombres (BOM)
- Mapea columnas
- Retorna: 7,753 registros
    ↓
FASE 2: VERSIÓN HISTÓRICA (7,752)

- Mantiene todos los períodos
- Guarda: RENIEC_Historico_Completo.xlsx
    ↓
FASE 3: VERSIÓN LIMPIA (1,027)

- Solo última versión
- Guarda: RENIEC_Datos_Consolidados_Limpios.xlsx
    ↓
LISTO: 2 archivos Excel
`text

---

## Cual archivo usar

HISTÓRICO:

- Archivo: RENIEC_Historico_Completo.xlsx
- Registros: 7,752
- Uso: Análisis temporal
- Power BI: Gráficas de línea

LIMPIO:

- Archivo: RENIEC_Datos_Consolidados_Limpios.xlsx
- Registros: 1,027
- Uso: Directorio actualizado
- Power BI: Dashboard de ubicaciones

---

## Cómo usar el sistema

### Paso 1: Ejecutar el script

`text
python Panda.py
`text

### Paso 2: Revisar resultados

Archivos en CVS/Extraccion de los datos/:

- RENIEC_Historico_Completo.xlsx (7,752 registros)
- RENIEC_Datos_Consolidados_Limpios.xlsx (1,027)
- Respaldos CSV

### Paso 3: Usar en Excel/Power BI

- Archivo histórico: análisis de tendencias
- Archivo limpio: directorio telefónico

---

## Personalización

### Escenario 1: Nuevo reporte de RENIEC

Editar config_archivos.py:

`text
'18. Reporte I Trimestre 2026': {
    'sep': ',',
    'skip': 0,
    'periodo': '2026-03-31'
}
`text

---

### Escenario 2: Nombre de columna diferente

Editar config_archivos.py:

`text
'NUEVA_VARIANTE': 'CENTRO DE ATENCION'
`text

---

### Escenario 3: Cambiar color de Excel

Editar config_archivos.py:

`text
'color_fondo': 'FF0000'  (Rojo)
`text

Colores: 366092 (Azul), FF0000 (Rojo), 008000 (Verde)

---

### Escenario 4: Cambiar ubicación de carpetas

Editar config_paths.py:

`text
RUTA_ORIGEN = os.path.join(parent, 'NUEVA_CARPETA')
`text

---

## Troubleshooting

### Error 1: ModuleNotFoundError: No module named pandas

Causa: Falta instalar dependencias

Solución:

`text
pip install pandas openpyxl
`text

---

### Error 2: No module named config_paths

Causa: Archivos no en la misma carpeta

Solución: Verifica que estén en Codigo Python/

---

### Error 3: El archivo histórico no tiene 7,752 registros

Causa: Un CSV no se procesó

Revisión:

- Abre Panda.py busca [ERROR]
- Verifica CONFIG_ARCHIVOS tenga PERIODO
- Revisa que CSV exista en CVS/

---

### Error 4: Las columnas no se mapean

Causa: Nombre no en MAPA_COLUMNAS

Solución: Agrega en config_archivos.py

`text
'NOMBRE_EXACTO': 'NOMBRE_ESTANDAR'
`text

---

### Error 5: Permission denied al guardar Excel

Causa: Archivo Excel abierto

Solución: Cierra Excel y ejecuta nuevamente

---

## Próximos Pasos

### Integración con SQL Server

```sql
CREATE TABLE TB_RENIEC_Historico (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    PERIODO DATE NOT NULL,
    DEPARTAMENTO VARCHAR(30),
    PROVINCIA VARCHAR(30),
    DISTRITO VARCHAR(30),
    CENTRO_ATENCION VARCHAR(90),
    ESTADO VARCHAR(20),
    HORARIOS VARCHAR(50),
    DIRECCION VARCHAR(150)
);
`text

---

### Integración con Power BI

1. Abre Power BI Desktop
2. Carga datos del Excel histórico
3. Crea visualizaciones:

   - Línea temporal
   - Mapa de centros
   - Tabla de directorio

---

## Checklist

- Mantén CSV en CVS/
- No renombres CSV
- Edita config_archivos.py para cambios
- Guarda backups
- Revisa logs en consola
- Mantén .venv actualizado

---

## Soporte

Si algo no funciona:

1. Lee el error completo
2. Revisa Troubleshooting
3. Verifica config_archivos.py
4. Comprueba CSV existan
5. Instala pandas si falta

---

Documentación completa y lista.
Última actualización: 11 de Enero de 2026
