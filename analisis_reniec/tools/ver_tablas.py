import pyodbc

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EDINSON\\EDINSON;Database=DW_RENIEC_Gestion;Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME")
print("=== TABLAS EN DW_RENIEC_Gestion ===\n")
for table in cursor.fetchall():
    name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM [{name}]")
    count = cursor.fetchone()[0]
    print(f"  • {name}: {count} registros")

print("\n=== MUESTRA DE DATOS (TB_RENIEC_HISTORICO) ===\n")
try:
    query = """
    SELECT TOP 5 
        PERIODO, 
        DEPARTAMENTO, 
        PROVINCIA, 
        DISTRITO
    FROM TB_RENIEC_HISTORICO
    ORDER BY PERIODO DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")
    else:
        print("  (sin registros)")
except Exception as e:
    print(f"  Error: {e}")

conn.close()
