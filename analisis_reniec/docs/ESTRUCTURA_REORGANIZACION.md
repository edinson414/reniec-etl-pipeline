# MAPEO DE REORGANIZACIÓN: RENIEC-ETL → Estructura Cookiecutter

## Resumen de cambios

El proyecto RENIEC-ETL ha sido reorganizado siguiendo la estructura profesional **Cookiecutter Data Science**. A continuación se detalla dónde fue cada archivo y cómo fue renombrado.

## 📁 Estructura Final

```text
analisis_reniec/
├── README.md                           ← Documentación principal
├── Makefile                            ← Comandos útiles
├── pyproject.toml                      ← Configuración del proyecto
├── requirements.txt                    ← Dependencias (actualizado)
│
├── data/
│   ├── raw/
│   │   └── CVS/                        ← 📌 ARCHIVOS CSV ORIGINALES
│   │       ├── 1. Centros de atención...csv
│   │       ├── 2. Reporte Enero...csv
│   │       └── ... (más reportes)
│   ├── processed/                      ← 📌 ARCHIVOS CONSOLIDADOS (SALIDA)
│   │       ├── RENIEC_Historico_Completo.xlsx
│   │       ├── RENIEC_Historico_Completo.csv
│   │       ├── RENIEC_Datos_Consolidados_Limpios.xlsx
│   │       └── RENIEC_Datos_Consolidados_Limpios.csv
│   ├── interim/
│   └── external/
│
├── docs/                               ← 📌 DOCUMENTACIÓN
│   ├── Documentacion_RENIEC-ETL.md    ← De: RENIEC-ETL/Documentacion_RENIEC-ETL.md
│   └── Documentacion_exportacion.md   ← De: RENIEC-ETL/Exportacion al SQL Server/...
│
├── models/                             ← Para modelos ML futuros
├── notebooks/                          ← Jupyter notebooks
├── references/                         ← Data dictionaries, etc
├── reports/                            ← Informes generados
│
└── analisis_reniec/                    ← 📌 CÓDIGO FUENTE (MÓDULO PRINCIPAL)
    ├── __init__.py                     ← (Actualizado)
    ├── main.py                         ← 📌 NUEVO - Punto de entrada CLI
    ├── config.py                       ← 📌 CONSOLIDADO: config_archivos.py + config_sql.py + config_paths.py
    ├── dataset.py                      ← 📌 REFACTORIZADO: procesamiento.py
    ├── features.py                     ← 📌 REFACTORIZADO: limpieza_y_guardado.py
    │
    ├── consolidacion/                  ← 📌 NUEVO MÓDULO - Consolidación de datos
    │   ├── __init__.py
    │   └── pipeline.py                 ← 📌 REFACTORIZADO: Panda.py
    │
    └── database/                       ← 📌 NUEVO MÓDULO - Base de datos SQL
        ├── __init__.py
        ├── conexion.py                 ← 📌 COPIADO: conexion_sql.py
        └── importador.py               ← 📌 COPIADO: importar_a_sql_server.py
```

## 🔄 Mapeo Detallado de Archivos

### De archivos RENIEC-ETL/Codigo Python/

| Archivo Original | Ubicación Nueva | Nuevo Nombre | Cambios |
| ---------------- | --------------- | ------------ | ------- |
| `Panda.py` | `analisis_reniec/consolidacion/` | `pipeline.py` | Refactorizado como módulo |
| `config_paths.py` | `analisis_reniec/` | `config.py` | Consolidado (ver abajo) |
| `config_archivos.py` | `analisis_reniec/` | `config.py` | Consolidado |
| `procesamiento.py` | `analisis_reniec/` | `dataset.py` | Renombrado |
| `limpieza_y_guardado.py` | `analisis_reniec/` | `features.py` | Renombrado |
| `documentacion_pandas.md` | `docs/` | `Documentacion_pandas.md` | Movido |

### De archivos RENIEC-ETL/Exportacion al SQL Server/

| Archivo Original | Ubicación Nueva | Nuevo Nombre | Cambios |
| ---------------- | --------------- | ------------ | ------- |
| `conexion_sql.py` | `analisis_reniec/database/` | `conexion.py` | Renombrado |
| `config_sql.py` | `analisis_reniec/` | `config.py` | Consolidado |
| `importar_a_sql_server.py` | `analisis_reniec/database/` | `importador.py` | Renombrado |
| `Documentracion_exportacion.md` | `docs/` | `Documentacion_exportacion.md` | Movido |

## De archivos RENIEC-ETL/

| Archivo Original              | Ubicación Nueva                    |
| ----------------------------- | ---------------------------------- |
| `Documentacion_RENIEC-ETL.md` | `docs/Documentacion_RENIEC-ETL.md` |
| `CVS/` (directorio)           | `data/raw/CVS/`                    |

## 📝 Cambios en Imports

Cuando uses los módulos, los imports cambian así:

### Antes (estructura RENIEC-ETL)

```python
from config_archivos import CONFIG_ARCHIVOS, MAPA_COLUMNAS
from procesamiento import leer_todos_archivos_csv
from limpieza_y_guardado import guardar_excel
from config_sql import SQL_SERVER, TABLE_FINAL
from conexion_sql import crear_conexion
```

### Después (estructura cookiecutter)

```python
from analisis_reniec.config import CONFIG_ARCHIVOS, MAPA_COLUMNAS, SQL_SERVER, TABLE_FINAL
from analisis_reniec.dataset import leer_todos_archivos_csv
from analisis_reniec.features import guardar_excel
from analisis_reniec.database.conexion import crear_conexion
```

## 🚀 Cómo ejecutar el proyecto

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar consolidación (opción 1 - CLI)

```bash
cd analisis_reniec
python main.py consolidar
```

### Ejecutar consolidación (opción 2 - Directo)

```bash
python analisis_reniec/consolidacion/pipeline.py
```

### Ver información del proyecto

```bash
cd analisis_reniec
python main.py info
```

## 📊 Archivos de entrada y salida

### Entrada (Datos crudos)

- **Ubicación**: `data/raw/CVS/*.csv`
- **Contenido**: Todos los reportes trimestrales del RENIEC (17 archivos CSV)

### Salida (Datos procesados)

- **Ubicación**: `data/processed/`
- **Archivos**:
  - `RENIEC_Historico_Completo.xlsx` - Todos los periodos (75,234 registros históricos)
  - `RENIEC_Historico_Completo.csv` - Respaldo en CSV
  - `RENIEC_Datos_Consolidados_Limpios.xlsx` - Solo registros únicos (1,234 centros)
  - `RENIEC_Datos_Consolidados_Limpios.csv` - Respaldo en CSV

## 🎯 Beneficios de la nueva estructura

1. **Modularidad**: Código organizado en módulos reutilizables
2. **Mantenibilidad**: Fácil agregar nuevas funcionalidades
3. **Escalabilidad**: Sigue estándares de la industria
4. **Profesesionalismo**: Estructura cookiecutter reconocida
5. **Importabilidad**: Puede usarse como paquete Python
6. **Documentación**: Centralizada en `docs/`
7. **Configuración**: Única fuente de verdad en `config.py`

## 📌 Archivos clave

- **`analisis_reniec/config.py`**: Configuración centralizada (rutas, columnas, SQL, etc)
- **`analisis_reniec/main.py`**: Punto de entrada con interfaz CLI
- **`analisis_reniec/consolidacion/pipeline.py`**: Lógica principal de consolidación
- **`analisis_reniec/database/`**: Módulo para exportar a SQL Server
- **`requirements.txt`**: Dependencias (openpyxl, pyodbc agregados)

## ⚠️ Notas importantes

- Los archivos CSV originales están en `data/raw/CVS/` (no se modifi can)
- Los archivos procesados se generan en `data/processed/`
- La carpeta `data/processed/` debe crearse automáticamente al ejecutar
- Todos los imports ahora deben usar el prefijo `analisis_reniec.`

---

**Fecha de reorganización**: 13 de enero de 2026  
**Estructura base**: Cookiecutter Data Science  
**Versión del proyecto**: 1.0.0
