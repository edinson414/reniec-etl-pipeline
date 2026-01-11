# Documentación del Proyecto RENIEC-ETL (Para principiantes)

Este documento explica en lenguaje sencillo qué hace este proyecto, cómo funciona y cómo usarlo, incluso si no tienes experiencia en programación.

---

## ¿Qué es este proyecto?

Este proyecto **consolida y limpia datos** de los centros de atención del RENIEC (Registro Nacional de Identificación y Estado Civil) que están distribuidos en múltiples archivos CSV con diferentes formatos.

**Objetivo principal:** Tomar muchos archivos CSV desorganizados y convertirlos en dos archivos Excel limpios y listos para usar:

1. **Archivo Histórico**: Contiene todos los registros de todos los periodos (ideal para análisis de tendencias en Power BI).
2. **Archivo Limpio**: Contiene solo la versión más reciente de cada centro (ideal para usar como directorio telefónico actualizado).

---

## ¿Qué problema resuelve?

Los archivos CSV del RENIEC vienen con diferentes problemas:

- Nombres de columnas diferentes (algunos dicen "CENTRO DE ATENCIÓN", otros "NOMBRE LOCAL").
- Diferentes separadores (algunos usan coma `,`, otros punto y coma `;`).
- Filas de encabezado que hay que saltar en algunos archivos.
- Duplicados: el mismo centro aparece en varios reportes trimestrales.
- Caracteres especiales y espacios que causan errores.

Este proyecto **automatiza la limpieza** de todos esos archivos y genera archivos consolidados sin errores.

---

## Estructura del proyecto

El proyecto se divide en dos carpetas principales:

### 1. **Codigo Python/** - Consolidación y limpieza de datos

Aquí están los scripts que procesan los archivos CSV y generan los archivos consolidados.

#### Archivos principales:

- **Panda.py** - Script principal que ejecuta todo el proceso.
- **config_paths.py** - Define dónde están los archivos de entrada y dónde se guardarán los resultados.
- **config_archivos.py** - Configuración de cada archivo CSV (separadores, periodos, columnas).
- **procesamiento.py** - Funciones para leer y procesar los CSV.
- **limpieza_y_guardado.py** - Funciones para limpiar duplicados y guardar Excel con formato.

### 2. **Exportacion al SQL Server/** - Carga a base de datos

Scripts para enviar los datos consolidados a una base de datos SQL Server.

- **importar_a_sql_server.py** - Script principal de exportación.
- **config_sql.py** - Configuración de conexión a SQL Server.
- **conexion_sql.py** - Funciones de conexión y carga.
- **Documentracion_exportacion.md** - Documentación específica para la exportación.

---

## ¿Cómo funciona el proceso de consolidación?

El proceso se ejecuta en **3 fases** cuando corres el script `Panda.py`:

### Fase 1: Lectura y Procesamiento

1. El script busca todos los archivos CSV en la carpeta `CVS/`.
2. Para cada archivo, identifica:
   - Qué separador usa (`,` o `;`).
   - Cuántas filas de encabezado debe saltar.
   - A qué periodo corresponde (ejemplo: 2024-03-31 para el primer trimestre 2024).
3. Lee el archivo y normaliza los nombres de las columnas (todos se convierten a mayúsculas y se eliminan acentos).
4. Mapea las columnas con diferentes nombres a un estándar común (ejemplo: "CENTRO DE ATENCIÓN" y "NOMBRE LOCAL" se convierten en "CENTRO DE ATENCION").
5. Selecciona solo las columnas necesarias: Departamento, Provincia, Distrito, Centro de Atención, Estado, Horarios, Dirección.
6. Agrega dos columnas adicionales:
   - **PERIODO**: fecha del reporte.
   - **ARCHIVO_ORIGEN**: nombre del archivo CSV original.

### Fase 2: Generación del Archivo Histórico

1. Toma todos los registros de todos los periodos.
2. Elimina **solo las filas completamente idénticas** (mismo centro, mismo periodo, misma dirección).
3. Guarda el resultado en:
   - `RENIEC_Historico_Completo.xlsx` (Excel formateado).
   - `RENIEC_Historico_Completo.csv` (CSV de respaldo).

**Ejemplo:** Si un centro aparece en 5 trimestres diferentes, las 5 versiones se mantienen en el histórico.

### Fase 3: Generación del Archivo Limpio

1. Toma todos los registros y los ordena por periodo (más reciente primero).
2. Elimina duplicados **mantiendo solo la versión más reciente** de cada centro.
3. El criterio de duplicado es: mismo Departamento, Provincia, Distrito y Centro de Atención.
4. Guarda el resultado en:
   - `RENIEC_Datos_Consolidados_Limpios.xlsx` (Excel formateado).
   - `RENIEC_Datos_Consolidados_Limpios.csv` (CSV de respaldo).

**Ejemplo:** Si un centro aparece en 5 trimestres, solo se guarda la versión del último trimestre.

---

## Requisitos para ejecutar el proyecto

### Software necesario:

- **Python 3** instalado (versión 3.8 o superior).
- Paquetes de Python: `pandas`, `openpyxl`.

### Instalación de paquetes (PowerShell):

```powershell
pip install pandas openpyxl
```

### Estructura de carpetas esperada:

```
RENIEC-ETL/
├── Codigo Python/
│   ├── Panda.py
│   ├── config_paths.py
│   ├── config_archivos.py
│   ├── procesamiento.py
│   └── limpieza_y_guardado.py
├── CVS/
│   ├── 1. Centros de atención del RENIEC a nivel nacional 2021.csv
│   ├── 2. Reporte Enero_Diciembre_2021.csv
│   ├── 3. Reporte I Semestre 2022.csv
│   ├── ... (más archivos CSV)
│   └── Extraccion de los datos/  (se crea automáticamente)
└── Exportacion al SQL Server/
    └── ... (scripts de exportación)
```

---

## Cómo ejecutar el proceso

### Paso 1: Coloca tus archivos CSV

Asegúrate de que todos los archivos CSV estén en la carpeta `CVS/` (al mismo nivel que `RENIEC-ETL/`).

### Paso 2: Ejecuta el script principal

Abre PowerShell, navega a la carpeta del código y ejecuta:

```powershell
cd "RENIEC-ETL/Codigo Python"
python Panda.py
```

### Paso 3: Revisa los resultados

El script mostrará mensajes de progreso en la consola. Al finalizar, encontrarás los archivos generados en:

```
CVS/Extraccion de los datos/
├── RENIEC_Historico_Completo.xlsx
├── RENIEC_Historico_Completo.csv
├── RENIEC_Datos_Consolidados_Limpios.xlsx
└── RENIEC_Datos_Consolidados_Limpios.csv
```

---

## Interpretación de los mensajes de consola

Durante la ejecución verás mensajes como estos:

- `[LEY] Leyendo: 10. Reporte I Trimestre 2024.csv` - Está leyendo un archivo CSV.
- `[OK] Procesado: 1,234 registros (Período: 2024-03-31)` - Se procesó correctamente.
- `[DEDUP] Histórico: 15,000 -> 14,856 registros` - Eliminó 144 filas completamente duplicadas.
- `[DEDUP] Limpio: 15,000 registros -> 1,234 únicos` - De 15,000 registros históricos, solo 1,234 son únicos.
- `[GUARDANDO] Versión Histórica...` - Está guardando el archivo Excel.
- `[OK] RENIEC_Historico_Completo.xlsx` - Archivo generado exitosamente.
- `[EXITO] PROCESO COMPLETADO` - Todo terminó correctamente.

---

## Archivos de configuración

### config_paths.py - Rutas de archivos

Define dónde buscar los CSV y dónde guardar los resultados. **No necesitas modificarlo** a menos que cambies la estructura de carpetas.

```python
RUTA_ORIGEN = 'CVS/'  # Carpeta con los archivos CSV
RUTA_DESTINO = 'CVS/Extraccion de los datos/'  # Carpeta de salida
```

### config_archivos.py - Configuración de cada CSV

Aquí se define cómo procesar cada archivo CSV. **Ejemplo:**

```python
CONFIG_ARCHIVOS = {
    '10. Reporte I Trimestre 2024': {
        'sep': ',',           # Separador de columnas
        'skip': 1,            # Filas de encabezado a saltar
        'periodo': '2024-03-31'  # Fecha del reporte
    },
    ...
}
```

Si agregas un nuevo archivo CSV, debes agregar su configuración aquí.

### Mapeo de columnas

El archivo también define cómo normalizar nombres de columnas:

```python
MAPA_COLUMNAS = {
    'CENTRO DE ATENCIÓN': 'CENTRO DE ATENCION',
    'NOMBRE LOCAL': 'CENTRO DE ATENCION',
    'HORARIO DE ATENCIÓN AL PUBLICO': 'HORARIOS',
    ...
}
```

Esto asegura que, sin importar cómo se llame la columna en el CSV, siempre se use el mismo nombre estándar.

---

## Formato del Excel generado

Los archivos Excel se guardan con formato profesional:

- **Encabezados**: Fondo azul oscuro, texto blanco, negrita.
- **Columnas ajustadas**: Anchos personalizados para cada columna.
- **Texto centrado y ajustado**: Fácil de leer.

### Columnas en el Histórico:

1. PERIODO
2. DEPARTAMENTO
3. PROVINCIA
4. DISTRITO
5. CENTRO DE ATENCION
6. ESTADO
7. HORARIOS
8. DIRECCION
9. ARCHIVO_ORIGEN

### Columnas en el Limpio:

1. DEPARTAMENTO
2. PROVINCIA
3. DISTRITO
4. CENTRO DE ATENCION
5. ESTADO
6. HORARIOS
7. DIRECCION

---

## Errores comunes y soluciones

### Error: `ModuleNotFoundError: No module named 'pandas'`

**Causa:** No tienes instalado el paquete `pandas`.

**Solución:**

```powershell
pip install pandas openpyxl
```

### Error: `FileNotFoundError: No se encuentra el archivo CSV`

**Causa:** Los archivos CSV no están en la carpeta `CVS/`.

**Solución:** Verifica que los archivos CSV estén en la ubicación correcta.

### Advertencia: `Columnas esperadas encontradas: ['DEPARTAMENTO', 'PROVINCIA']`

**Causa:** El archivo CSV tiene un formato diferente al esperado.

**Solución:** Revisa el archivo CSV y actualiza `config_archivos.py` con el separador y mapeo correctos.

### El proceso termina pero no genera archivos

**Causa:** No se pudieron leer archivos CSV o todos dieron error.

**Solución:** Revisa los mensajes de error en la consola para identificar qué archivos fallaron.

---

## Mantenimiento: Agregar nuevos archivos CSV

Si RENIEC publica un nuevo reporte trimestral:

1. **Descarga el archivo CSV** y colócalo en la carpeta `CVS/`.

2. **Abre `config_archivos.py`** y agrega una entrada para el nuevo archivo:

```python
'18. Reporte I Trimestre 2026': {
    'sep': ',',              # Prueba primero con coma
    'skip': 1,               # Salta 1 fila de encabezado
    'periodo': '2026-03-31'  # Fecha del trimestre
},
```

3. **Ejecuta nuevamente `Panda.py`** para regenerar los archivos consolidados.

---

## Exportación a SQL Server

Una vez que tengas los archivos consolidados, puedes exportarlos a una base de datos SQL Server para consultas y análisis avanzados.

**Consulta la documentación específica:**

- [Documentracion_exportacion.md](Exportacion%20al%20SQL%20Server/Documentracion_exportacion.md)

Allí encontrarás:

- Configuración de conexión a SQL Server.
- Cómo ejecutar la importación.
- Solución de errores comunes.

---

## Resumen de uso rápido

```powershell
# 1. Instalar dependencias (solo una vez)
pip install pandas openpyxl

# 2. Ejecutar el proceso de consolidación
cd "RENIEC-ETL/Codigo Python"
python Panda.py

# 3. Los archivos se generan en:
# CVS/Extraccion de los datos/
```

---

## Preguntas frecuentes

### ¿Por qué dos archivos (Histórico y Limpio)?

- **Histórico**: Para análisis de tendencias (¿cuántos centros abrieron/cerraron en cada trimestre?).
- **Limpio**: Para tener un directorio actualizado sin duplicados.

### ¿Puedo modificar las columnas que se exportan?

Sí, edita las listas `COLUMNAS_HISTORICO` y `COLUMNAS_LIMPIO` en `config_archivos.py`.

### ¿Los archivos CSV originales se modifican?

No, el proceso solo lee los archivos originales y genera nuevos archivos consolidados.

### ¿Qué pasa si hay centros con el mismo nombre en diferentes departamentos?

El proceso de deduplicación considera: Departamento + Provincia + Distrito + Nombre del Centro. Si dos centros tienen el mismo nombre pero están en diferentes distritos, se mantienen ambos.

### ¿Puedo ejecutar el proceso varias veces?

Sí, el proceso sobrescribe los archivos generados, así que puedes ejecutarlo cuantas veces quieras sin problema.

---

## Soporte y ayuda

Si encuentras errores o tienes dudas:

1. Revisa los mensajes de error en la consola.
2. Verifica que los archivos CSV estén en la carpeta correcta.
3. Comprueba que los paquetes estén instalados: `pip list | findstr pandas`.
4. Revisa la configuración en `config_archivos.py`.

Para ayuda adicional, comparte:

- El mensaje de error completo.
- El nombre del archivo CSV problemático.
- La salida de la consola.

---

## Créditos

Este proyecto automatiza la consolidación de datos públicos del RENIEC para facilitar su análisis y uso en herramientas de Business Intelligence como Power BI o bases de datos SQL Server.
