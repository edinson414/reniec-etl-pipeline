# Documentación de Exportación a SQL Server (No programadores)

Este documento explica, en lenguaje sencillo, cómo el proyecto carga la información histórica de centros de atención del RENIEC a una base de datos SQL Server. Está pensado para que personas sin conocimientos de programación puedan entender qué ocurre y cómo ejecutar el proceso con seguridad.

## Objetivo

- Cargar el archivo histórico consolidado en CSV a SQL Server.
- Crear una tabla temporal de carga (staging), una tabla final con índices y transferir los datos.
- Validar que la cantidad de registros cargados coincida con el archivo de origen.

## Qué se importa

- Archivo principal: RENIEC_Historico_Completo.csv
- Ubicación prevista: carpeta CVS/Extraccion de los datos. La ruta exacta está configurada en el archivo de configuración.

## Estructura de esta carpeta

- importar_a_sql_server.py: Orquesta todo el proceso de importación (paso a paso).
- conexion_sql.py: Contiene las funciones para conectarse a SQL Server, crear tablas, insertar datos y validar.
- config_sql.py: Archivo de configuración (servidor, base de datos, rutas de archivo, esquema de tabla e índices).

Puede verlos aquí:
- RENIEC-ETL/Exportacion al SQL Server/importar_a_sql_server.py
- RENIEC-ETL/Exportacion al SQL Server/conexion_sql.py
- RENIEC-ETL/Exportacion al SQL Server/config_sql.py

## Requisitos previos

- SQL Server disponible y accesible (local o remoto) y base de datos creada.
- Driver ODBC de SQL Server instalado (recomendado: ODBC Driver 17 for SQL Server).
- Python 3 instalado en el equipo (con permisos para instalar paquetes).
- Paquetes Python: pyodbc y pandas.
- Permisos de escritura en la base de datos para crear tablas e índices.

Instalación rápida de paquetes (Windows PowerShell):

```powershell
pip install pyodbc pandas
```

## Configuración (sin tocar código)

Todo se configura en: RENIEC-ETL/Exportacion al SQL Server/config_sql.py

- SQL_SERVER: Nombre de servidor SQL. Ej.: EDINSON\EDINSON
- SQL_DATABASE: Nombre de la base de datos destino. Ej.: DW_RENIEC_Gestion
- SQL_DRIVER: Driver ODBC a usar. Ej.: ODBC Driver 17 for SQL Server
- SQL_TRUSTED_CONNECTION: true para autenticación de Windows; false para usuario/contraseña SQL.
- SQL_USERNAME / SQL_PASSWORD: Solo si usa autenticación SQL (cuando SQL_TRUSTED_CONNECTION es false).
- ARCHIVO_CSV_HISTORICO: Ruta al CSV consolidado a importar.
- BATCH_SIZE: Tamaño de lote para insertar más rápido (por defecto 1000).
- TIMEOUT: Tiempo de espera de la conexión (segundos).
- SCHEMA_TABLA: Lista de columnas y tipos que se crearán en SQL Server.
- INDICES: Índices que se crearán en la tabla final para acelerar consultas.

## Columnas esperadas

En la tabla final se crean, entre otras, estas columnas:

- PERIODO: Fecha del periodo (se convierte a formato fecha AAAA-MM-DD).
- DEPARTAMENTO, PROVINCIA, DISTRITO: Ubicación geográfica.
- CENTRO_ATENCION: Nombre del centro (si el CSV trae "CENTRO DE ATENCION", se renombra automáticamente).
- ESTADO: Estado operativo del centro.
- HORARIOS: Horarios de atención.
- DIRECCION: Dirección física.
- ARCHIVO_ORIGEN: De qué archivo provino el registro.

Nota: Si el CSV trae una columna FECHA_CARGA, el proceso la omite porque SQL Server la puede generar por su cuenta.

## Qué hace el proceso, paso a paso

Cuando se ejecuta importar_a_sql_server.py, se realizan estos pasos:

1. Verifica que el archivo CSV configurado exista.
2. Se conecta a SQL Server con los parámetros de config_sql.py.
3. Crea una tabla temporal (staging) desde cero para recibir los datos del CSV.
4. Lee el CSV y limpia datos básicos (fechas, espacios, valores vacíos) y los inserta en lotes en la tabla staging.
5. Crea la tabla final con una columna ID autoincremental e índices para consultas rápidas.
6. Copia todos los registros desde la tabla staging a la tabla final.
7. Compara cuántos registros hay en el CSV y en la tabla final para validar la carga.
8. Elimina la tabla staging (limpieza) para dejar solo la tabla final.

Tablas creadas:

- Temporal: TB_RENIEC_Historico_Stg (se elimina al finalizar).
- Final: TB_RENIEC_Historico (permanece con índices creados).

## Cómo ejecutarlo

Desde la carpeta RENIEC-ETL/Exportacion al SQL Server, ejecute:

```powershell
python importar_a_sql_server.py
```

Si todo está correcto, verá mensajes de avance y al final un resumen con la cantidad de registros transferidos y la confirmación de validación.

## Mensajes y validación

- Los mensajes [OK] indican pasos completados con éxito (conexión, creación de tablas, inserciones, etc.).
- La validación compara el número de filas del CSV con la tabla final en SQL.
- Si hay diferencias, se mostrará una advertencia para revisar el CSV u hojas de transformación previas.

## Errores frecuentes y soluciones

- No se pudo conectar a SQL Server: Verifique servidor, base de datos, driver ODBC y permisos.
- Driver ODBC no encontrado: Instale "ODBC Driver 17 for SQL Server".
- No se encuentra el archivo CSV: Revise la ruta configurada en config_sql.py.
- Permisos insuficientes para crear tablas/índices: Solicite permisos al administrador de la base.
- Error en inserción de un lote: El proceso intenta identificar filas problemáticas e informa cuáles son.

## Rendimiento y seguridad

- Rendimiento: Inserta en lotes (BATCH_SIZE) y usa un modo rápido de inserción para grandes volúmenes.
- Seguridad: Con autenticación de Windows, los permisos dependen del usuario actual de Windows. Si requiere usuario SQL, configure SQL_USERNAME/SQL_PASSWORD y desactive Trusted Connection.

## Mantenimiento y cambios futuros

- Nueva columna en el CSV: Agréguela también en SCHEMA_TABLA con su tipo SQL, ajuste cualquier renombrado necesario y, si aplica, cree un índice.
- Cambiar nombres de tablas: Modifique TABLE_STAGING y TABLE_FINAL en config_sql.py.
- Cambiar rutas: Actualice ARCHIVO_CSV_HISTORICO.

## Soporte

Si necesita ayuda para ajustar la configuración o resolver errores, comparta:

- El mensaje de error exacto mostrado por la consola.
- La configuración relevante de config_sql.py (sin contraseñas).
- Confirmación de que el driver ODBC y los permisos existen.
