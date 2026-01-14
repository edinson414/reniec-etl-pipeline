import pyodbc

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EDINSON\\EDINSON;DATABASE=DW_RENIEC_Gestion;Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Listar tablas
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
print("=== TABLAS EN LA BASE DE DATOS ===\n")
for table in cursor.fetchall():
    print(f"  • {table[0]}")

print("\n=== CONTEO DE REGISTROS ===\n")
for table in ["TB_RENIEC_LIMPIO", "TB_RENIEC_HISTORICO"]:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} registros")
    except Exception as e:
        print(f"{table}: NO EXISTE ({str(e)[:50]})")

print("\n=== VERIFICACIÓN DE CARACTERES ESPECIALES ===\n")
try:
    query = """
    SELECT TOP 10 
        PERIODO, 
        DEPARTAMENTO, 
        PROVINCIA, 
        DISTRITO, 
        DIRECCION
    FROM TB_RENIEC_HISTORICO
    WHERE PROVINCIA LIKE '%FERREÑAFE%' OR DEPARTAMENTO LIKE '%APURÍMAC%'
    ORDER BY PERIODO DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"PERIODO: {row[0]}")
            print(f"DEPARTAMENTO: {row[1]}")
            print(f"PROVINCIA: {row[2]}")
            print(f"DISTRITO: {row[3]}")
            print(f"DIRECCIÓN: {row[4]}")
            print("---")
    else:
        print("No se encontraron registros con FERREÑAFE o APURÍMAC")
except Exception as e:
    print(f"Error: {e}")

conn.close()
