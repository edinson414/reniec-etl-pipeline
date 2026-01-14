import pyodbc

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EDINSON\\EDINSON;Database=DW_RENIEC_Gestion;Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Crear tabla
create_table_sql = """
IF NOT EXISTS (SELECT 1 FROM sys.objects WHERE type = 'U' AND name = 'TB_RENIEC_HISTORICO')
BEGIN
    CREATE TABLE [TB_RENIEC_HISTORICO] (
        [PERIODO] DATE NOT NULL,
        [DEPARTAMENTO] VARCHAR(30),
        [PROVINCIA] VARCHAR(30),
        [DISTRITO] VARCHAR(30),
        [CENTRO_ATENCION] VARCHAR(90),
        [ESTADO] VARCHAR(100),
        [HORARIOS] VARCHAR(150),
        [DIRECCION] VARCHAR(150),
        [ARCHIVO_ORIGEN] VARCHAR(100)
    );
    PRINT 'Tabla creada exitosamente';
END
ELSE
BEGIN
    PRINT 'La tabla ya existe';
END
"""

cursor.execute(create_table_sql)
conn.commit()

# Verificar que la tabla existe
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'TB_RENIEC_HISTORICO'")
result = cursor.fetchone()
if result:
    print(f"✅ Tabla {result[0]} verificada")
else:
    print("❌ Error: Tabla no creada")

conn.close()
