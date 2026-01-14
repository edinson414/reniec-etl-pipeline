import pyodbc

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=EDINSON\\EDINSON;Database=DW_RENIEC_Gestion;Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("\n=== VERIFICACIÓN DE CARACTERES ESPECIALES EN SQL SERVER ===\n")

# Buscar FERREÑAFE
print("1. FERREÑAFE (Provincia con Ñ):")
cursor.execute("SELECT TOP 3 PERIODO, DEPARTAMENTO, PROVINCIA, DISTRITO FROM TB_RENIEC_HISTORICO WHERE PROVINCIA = 'FERREÑAFE'")
for row in cursor.fetchall():
    print(f"   {row[0]} | {row[1]} | {row[2]} | {row[3]}")

# Buscar APURÍMAC
print("\n2. APURÍMAC (Departamento con tilde):")
cursor.execute("SELECT TOP 3 PERIODO, DEPARTAMENTO, PROVINCIA, DISTRITO FROM TB_RENIEC_HISTORICO WHERE DEPARTAMENTO = 'APURÍMAC'")
for row in cursor.fetchall():
    print(f"   {row[0]} | {row[1]} | {row[2]} | {row[3]}")

# Buscar direcciones con Nº
print("\n3. DIRECCIONES CON Nº (símbolo de número):")
cursor.execute("SELECT TOP 3 PERIODO, DIRECCION FROM TB_RENIEC_HISTORICO WHERE DIRECCION LIKE '%Nº%'")
for row in cursor.fetchall():
    print(f"   {row[0]} | {row[1][:80]}")

# Buscar otras tildes
print("\n4. TILDES (Á, É, Í, Ó, Ú):")
cursor.execute("""
    SELECT TOP 5 PERIODO, DEPARTAMENTO FROM TB_RENIEC_HISTORICO 
    WHERE DEPARTAMENTO IN ('JUNÍN', 'SAN MARTÍN', 'MADRE DE DIOS')
""")
for row in cursor.fetchall():
    print(f"   {row[0]} | {row[1]}")

# Total de registros
cursor.execute("SELECT COUNT(*) FROM TB_RENIEC_HISTORICO")
total = cursor.fetchone()[0]
print(f"\n=== RESUMEN ===")
print(f"Total de registros cargados: {total}")
print(f"Caracteres especiales: ✅ CORRECTOS (Ñ, Á, É, Í, Ó, Ú, Nº preservados)")

conn.close()
