# 📚 Guía Completa de Proyecto RENIEC

¡Bienvenido! Esta guía te explicará **paso a paso** cómo funcionan los análisis de datos del RENIEC, sin necesidad de entender código de programación.

---

## � Fuente de Datos

Este proyecto utiliza el **Dataset Abierto** oficial del Gobierno Peruano:

[RENIEC - Centros de Atención de RENIEC a Nivel Nacional](https://www.datosabiertos.gob.pe/dataset/reniec-centros-de-atención-del-reniec-nivel-nacional-registro-nacional-de-identificación-y)

---

## �📖 Índice

1. [¿Qué es este proyecto?](#qué-es-este-proyecto)
2. [¿Qué necesito para empezar?](#qué-necesito-para-empezar)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Cómo Ejecutar el Proyecto](#cómo-ejecutar-el-proyecto)
5. [Explicación de Cada Paso](#explicación-de-cada-paso)
6. [Verificación de Datos](#verificación-de-datos)
7. [Preguntas Frecuentes](#preguntas-frecuentes)
8. [Solución de Problemas](#solución-de-problemas)

---

## ¿Qué es este proyecto?

Este proyecto toma información sobre los **centros de atención del RENIEC** (lugares donde atienden documentos de identidad) desde el año 2021 hasta 2025.

### Lo que hace el proyecto

- ✅ **Lee** archivos Excel (.csv) con la lista de centros RENIEC
- ✅ **Organiza** los datos de forma limpia y ordenada
- ✅ **Guarda** la información en una **base de datos SQL Server** (una especie de archivo mega-organizado)
- ✅ **Permite** hacer análisis y reportes con esta información

---

## ¿Qué necesito para empezar?

### Software Requerido

1. **Python 3.10 o superior** (un lenguaje de programación)
   - Descarga desde: [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Durante la instalación, marca la opción **"Add Python to PATH"**

2. **SQL Server** (gestor de base de datos)
   - Ya debe estar instalado en tu computadora

3. **Una terminal o línea de comandos**
   - Windows: PowerShell o CMD
   - Recomendado: Terminal nativa de Windows

4. **VS Code** (editor de código - opcional pero recomendado)
   - Descarga desde: [https://code.visualstudio.com/](https://code.visualstudio.com/)

### Librerías Python Necesarias

Las siguientes librerías ya están instaladas en el proyecto, pero si necesitas instalarlas manualmente:

```bash
pip install pandas pyodbc openpyxl click
```

**Explicación simple:**

- `pandas`: Lee y procesa archivos Excel
- `pyodbc`: Se conecta a SQL Server
- `openpyxl`: Crea archivos Excel bonitos
- `click`: Hace que sea fácil ejecutar comandos

---

## Estructura del Proyecto

```text
analisis_reniec/                    (Carpeta principal del proyecto)
│
├── data/                           (Carpeta con DATOS)
│   ├── raw/                        (Datos originales - NO TOCAR)
│   │   ├── 1. Centros de atención del RENIEC a nivel nacional 2021.csv
│   │   ├── 2. Reporte Enero_Diciembre_2021.csv
│   │   └── ... (15 archivos más)
│   │
│   └── processed/                  (Datos ya procesados - RESULTADO FINAL)
│       ├── RENIEC_Historico_Completo.csv
│       ├── RENIEC_Historico_Completo.xlsx
│       ├── RENIEC_Datos_Consolidados_Limpios.csv
│       └── RENIEC_Datos_Consolidados_Limpios.xlsx
│
├── analisis_reniec/                (Código del proyecto)
│   ├── config.py                   (Configuración general)
│   ├── dataset.py                  (Lee los archivos CSV)
│   ├── features.py                 (Limpia y organiza datos)
│   ├── main.py                     (Archivo principal para ejecutar)
│   ├── consolidacion/              (Subcarpeta de consolidación)
│   │   └── pipeline.py             (El motor que procesa todo)
│   └── database/                   (Subcarpeta de base de datos)
│       └── export_sql.py           (Envía datos a SQL Server)
│
├── tools/                          (Scripts de verificación)
│   ├── ver_tablas.py               (Ve las tablas en SQL Server)
│   ├── verificar_caracteres.py     (Verifica que Ñ y tildes estén bien)
│   ├── verificar_sql.py            (Diagnóstico general)
│   └── crear_tabla.py              (Crea tabla manualmente)
│
├── docs/                           (Documentación - AQUÍ ESTÁS)
│   └── GUIA_COMPLETA.md
│
└── CVS/                            (Archivos originales sin procesar)
    └── ... (archivos históricos)
```

---

## Cómo Ejecutar el Proyecto

### Paso 1: Abre la Terminal

**En Windows:**

- Presiona `Windows + R`
- Escribe `cmd` o `powershell`
- Presiona Enter

### Paso 2: Navega a la Carpeta del Proyecto

Copia y pega este comando en la terminal:

```bash
cd "C:\Users\PC\Documents\Analicis de datos\2. RENIEC - Centros de atención del RENIEC a nivel nacional [Registro Nacional de Identificación y Estado Civil]\analisis_reniec"
```

**Explicación:** Esto te lleva a la carpeta donde está el proyecto.

### Paso 3: Ejecuta la Consolidación de Datos

Copia y pega este comando:

```bash
python -m analisis_reniec.main consolidar
```

**¿Qué sucede?**

1. El programa lee los 17 archivos CSV con datos de RENIEC
2. Los limpia y organiza
3. Crea 4 archivos en la carpeta `data/processed/`:
   - 2 archivos Excel (.xlsx)
   - 2 archivos CSV (.csv)

**Espera:** El proceso tarda entre 10-30 segundos. Verás mensajes en la pantalla diciendo que está leyendo archivos.

### Paso 4: Exporta los Datos a SQL Server

Después de que termine el paso anterior, ejecuta:

```bash
python -m analisis_reniec.database.export_sql
```

**¿Qué sucede?**

1. Lee el archivo CSV limpio que se creó
2. Se conecta a SQL Server (base de datos)
3. Crea una tabla llamada `TB_RENIEC_HISTORICO`
4. Carga los 7,752 registros en esa tabla

**Espera:** Debería terminar en 5-10 segundos.

### Paso 5: Verifica que Todo Esté Bien

Ejecuta este comando para verificar:

```bash
python tools/verificar_caracteres.py
```

**¿Qué sucede?**

- Te muestra que los datos se cargaron correctamente
- Verifica que caracteres especiales como Ñ, Á, É funcionen bien

---

## Explicación de Cada Paso

### 📊 PASO 1: Consolidación de Datos (El "Barrido")

**¿Qué es?**

Imagina que tienes 17 cajones diferentes con papeles (archivos CSV). El programa abre cada cajón, agarra todos los papeles, y los mete en un solo cajón MEGA-organizado.

**¿Qué archivos lee?**

- Datos de 2021 a 2025
- Total: 17 archivos CSV
- Total: 7,753 centros RENIEC

**¿Qué archivos crea?**

1. **RENIEC_Historico_Completo** (7,752 registros)
   - Contiene TODOS los centros de TODAS las épocas
   - Sirve para ver tendencias en el tiempo
   - Útil para: Reportes históricos, gráficos de tendencias

2. **RENIEC_Datos_Consolidados_Limpios** (988 registros)
   - Contiene SOLO los centros actuales (más recientes)
   - Sin duplicados
   - Útil para: Directorio actualizado, listados actuales

**¿Cómo limpia los datos?**

- Quita espacios en blanco extras
- Corrige problemas de codificación (Ñ, tildes, etc.)
- Elimina registros duplicados
- Organiza las columnas en orden

### 🗄️ PASO 2: Exportación a SQL Server (El "Almacén")

**¿Qué es SQL Server?**

Es un programa que guarda datos de forma mega-organizada, como un archivo de Excel pero mucho más potente.

**¿Qué sucede en este paso?**

1. Lee el archivo CSV limpio
2. Se conecta a SQL Server
3. Crea una tabla (como una hoja de Excel) llamada `TB_RENIEC_HISTORICO`
4. Copia todos los 7,752 registros en esa tabla

**¿Por qué hacer esto?**

- Los datos en SQL Server son más seguros
- Son más rápidos de buscar
- Se pueden hacer reportes complejos
- Múltiples personas pueden acceder al mismo tiempo

**¿Qué columnas tiene la tabla?**

| Columna         | Tipo  | Ejemplo                 |
| --------------- | ----- | ----------------------- |
| PERIODO         | Fecha | 2025-12-31              |
| DEPARTAMENTO    | Texto | LAMBAYEQUE              |
| PROVINCIA       | Texto | FERREÑAFE               |
| DISTRITO        | Texto | FERREÑAFE               |
| CENTRO_ATENCION | Texto | AG FERREÑAFE            |
| ESTADO          | Texto | OPERATIVO               |
| HORARIOS        | Texto | 08:45 - 16:45           |
| DIRECCION       | Texto | Jr. Bolognesi Nº 428    |
| ARCHIVO_ORIGEN  | Texto | 1. Centros... 2021.csv  |

---

## Verificación de Datos

Después de ejecutar todo, **siempre** verifica que los datos se cargaron bien.

### Verificación Rápida

```bash
python tools/verificar_caracteres.py
```

Este comando te mostrará:

- ✅ Que "FERREÑAFE" está escrito correctamente (con Ñ, no con ¥)
- ✅ Que "APURÍMAC" tiene la tilde bien
- ✅ Que el símbolo "Nº" está correcto
- ✅ El total de 7,752 registros cargados

**Resultado esperado:**

```text
=== VERIFICACIÓN DE CARACTERES ESPECIALES EN SQL SERVER ===

1. FERREÑAFE (Provincia con Ñ):
   2021-01-01 | LAMBAYEQUE | FERREÑAFE | FERREÑAFE
   ...

=== RESUMEN ===
Total de registros cargados: 7752
Caracteres especiales: ✅ CORRECTOS
```

### Verificación Completa

```bash
python tools/ver_tablas.py
```

Este comando muestra:

- Todas las tablas en la base de datos
- Cuántos registros tiene cada tabla
- Una muestra de los primeros 5 registros

---

## Preguntas Frecuentes

### P: ¿Cuánto tiempo tarda todo el proceso?

**R:** Aproximadamente:

- Consolidación: 10-30 segundos
- Exportación a SQL: 5-10 segundos
- Verificación: 2-5 segundos
- **Total: 20-45 segundos**

### P: ¿Qué pasa si ejecuto el comando dos veces?

**R:**

- La consolidación generará los mismos archivos (sobreescribe los antiguos)
- La exportación a SQL borrará la tabla antigua y creará una nueva
- No hay problema, puedes ejecutar cuantas veces quieras

### P: ¿Dónde veo los archivos generados?

**R:** En la carpeta `data/processed/`:

- `RENIEC_Historico_Completo.xlsx` (Excel)
- `RENIEC_Historico_Completo.csv` (para abrir en cualquier programa)
- `RENIEC_Datos_Consolidados_Limpios.xlsx` (Excel)
- `RENIEC_Datos_Consolidados_Limpios.csv` (para SQL)

### P: ¿Puedo abrir los archivos Excel mientras se ejecuta?

**R:**

- **NO**: Si tienes abierto el archivo mientras se ejecuta, puede haber error
- **SÍ**: Cierra los archivos antes de ejecutar, y ábrelos después

### P: ¿Qué significan las columnas?

**R:**

- **PERIODO**: Fecha del reporte (cuándo se hizo el reporte)
- **DEPARTAMENTO**: Región del Perú (Lambayeque, Piura, etc.)
- **PROVINCIA**: Ciudad pequeña dentro del departamento
- **DISTRITO**: Pueblo o zona dentro de la provincia
- **CENTRO_ATENCION**: Nombre específico del centro RENIEC
- **ESTADO**: Si está abierto (OPERATIVO) o cerrado
- **HORARIOS**: A qué hora atiende
- **DIRECCION**: Dónde está ubicado
- **ARCHIVO_ORIGEN**: De cuál archivo CSV viene esta información

### P: ¿Es seguro eliminar archivos?

**R:**

- ❌ **NO** elimines la carpeta `data/raw/` (contiene los datos originales)
- ❌ **NO** elimines los archivos CSV en `data/raw/`
- ✅ **SÍ** puedes eliminar los archivos en `data/processed/` (se regeneran solos)

---

## Solución de Problemas

### ❌ Error: "No se encontró el módulo 'pandas'"

**Solución:**

```bash
pip install pandas pyodbc openpyxl click
```

**¿Por qué ocurre?**

Las librerías de Python no están instaladas en tu computadora.

### ❌ Error: "No se ha podido resolver la importación"

**Solución:**

Este es solo un aviso de VS Code, pero **el programa funciona correctamente**. Puedes ignorarlo.

Para hacerlo desaparecer, presiona `Ctrl + Shift + P` en VS Code y busca:

```text
Python: Select Interpreter
```

Elige el Python que tiene instalados pandas y pyodbc.

### ❌ Error: "Invalid object name 'TB_RENIEC_HISTORICO'"

**Solución:**

La tabla no existe en SQL Server. Ejecuta:

```bash
python tools/crear_tabla.py
```

Esto crea la tabla manualmente.

### ❌ Error: "Conectado a SQL Server pero no se ve la tabla"

**Solución:**

Ejecuta nuevamente:

```bash
python -m analisis_reniec.database.export_sql
```

Si el error persiste, contacta al administrador de SQL Server.

### ❌ Error: "Caracteres raros como ¥ en lugar de Ñ"

**Solución:**

El problema de codificación ya fue resuelto. Simplemente:

1. Elimina los archivos en `data/processed/`
2. Vuelve a ejecutar:

```bash
python -m analisis_reniec.main consolidar
```

### ❌ La terminal no encuentra el comando

**Solución:**

Asegúrate de estar en la carpeta correcta:

```bash
cd "C:\Users\PC\Documents\Analicis de datos\2. RENIEC - Centros de atención del RENIEC a nivel nacional [Registro Nacional de Identificación y Estado Civil]\analisis_reniec"
```

Que Python esté instalado:

```bash
python --version
```

Si no reconoce `python`, intenta con `python3`:

```bash
python3 --version
```

---

## Resumen de Comandos

**Tabla rápida de referencia:**

| Objetivo | Comando |
| -------- | ------- |
| Consolidar datos | `python -m analisis_reniec.main consolidar` |
| Exportar a SQL | `python -m analisis_reniec.database.export_sql` |
| Ver tablas SQL | `python tools/ver_tablas.py` |
| Verificar caracteres | `python tools/verificar_caracteres.py` |
| Diagnóstico SQL | `python tools/verificar_sql.py` |
| Crear tabla manual | `python tools/crear_tabla.py` |
| Ver versión Python | `python --version` |
| Instalar librerías | `pip install pandas pyodbc openpyxl click` |

---

## Próximos Pasos

Una vez que tengas los datos en SQL Server, puedes:

- ✅ Crear reportes en Power BI
- ✅ Hacer gráficos de tendencias
- ✅ Buscar centros específicos
- ✅ Analizar cambios en el tiempo
- ✅ Exportar a otros formatos

---

## Contacto y Soporte

Si tienes dudas:

- 📧 Email: <edinsonalexandersaldarriaga@gmail.com>
- 📞 Teléfono: +51 980 520 086

---

**Última actualización:** 13 de enero de 2026
**Versión del proyecto:** 1.0.0
**Estado:** ✅ Producción (listo para usar)

---

¡Gracias por usar este proyecto! 🚀
