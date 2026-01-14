# 🛠️ Scripts de Verificación y Mantenimiento

Carpeta dedicada para scripts utilitarios de verificación y mantenimiento de la base de datos.

## Archivos

### 📊 `ver_tablas.py`

Verifica todas las tablas en `DW_RENIEC_Gestion` y muestra el conteo de registros.

**Uso:**

```bash
python tools/ver_tablas.py
```

**Salida:**

- Lista de tablas con cantidad de registros
- Muestra de datos (TOP 5 registros)

### ✅ `verificar_caracteres.py`

Valida que los caracteres especiales (Ñ, tildes, Nº) se preservaron correctamente en SQL Server.

**Uso:**

```bash
python tools/verificar_caracteres.py
```

**Verifica:**

- FERREÑAFE (Ñ correcta)
- APURÍMAC (tildes correctas)
- Nº en direcciones
- Otras tildes (JUNÍN, SAN MARTÍN, MADRE DE DIOS)

### 🔍 `verificar_sql.py`

Script diagnóstico para verificar estado de las tablas y conectividad a SQL Server.

**Uso:**

```bash
python tools/verificar_sql.py
```

### 🏗️ `crear_tabla.py`

Crea manualmente la tabla `TB_RENIEC_HISTORICO` en caso de ser necesario.

**Uso:**

```bash
python tools/crear_tabla.py
```

⚠️ **Nota:** Normalmente se crea automáticamente al ejecutar `export_sql.py`

## Ejecución desde cualquier ubicación

Si estás fuera de la carpeta del proyecto, especifica la ruta completa:

```bash
cd "C:\Users\PC\Documents\Analicis de datos\2. RENIEC - Centros de atención del RENIEC a nivel nacional [Registro Nacional de Identificación y Estado Civil]\analisis_reniec"
python tools/ver_tablas.py
```

## Conexión a SQL Server

Todos los scripts utilizan:

- **Servidor:** `EDINSON\EDINSON`
- **Base de datos:** `DW_RENIEC_Gestion`
- **Autenticación:** Windows (Trusted_Connection)

Si necesitas cambiar estos parámetros, edita la línea de conexión en cada script:

```python
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EDINSON\\EDINSON;Database=DW_RENIEC_Gestion;Trusted_Connection=yes;'
```
