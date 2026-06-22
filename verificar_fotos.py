import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:/sysflor/scae10-python/database/SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Buscar alunos com foto
cursor.execute("""
    SELECT ID, NOME, FOTO_PATH 
    FROM ALUNOS 
    WHERE FOTO_PATH IS NOT NULL 
    AND FOTO_PATH <> ''
    ROWS 5
""")

rows = cursor.fetchall()
print(f"Encontrados {len(rows)} alunos com foto:")
print("=" * 80)

for row in rows:
    print(f"ID: {row[0]}")
    print(f"NOME: {row[1]}")
    print(f"FOTO_PATH: {row[2]}")
    print("-" * 80)

conn.close()
