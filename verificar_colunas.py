import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()
cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ALUNOS'
    ORDER BY RDB$FIELD_POSITION
""")

print("Colunas da tabela ALUNOS:")
for row in cursor.fetchall():
    print(f"  {row[0].strip()}")

conn.close()
