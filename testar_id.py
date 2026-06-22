import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()
cursor.execute("SELECT ID, NOME FROM ALUNOS WHERE ATIVO = 'S' ORDER BY NOME ROWS 5")

print("Primeiros 5 alunos:")
for row in cursor.fetchall():
    print(f"  ID={row[0]} (tipo: {type(row[0])}) | NOME={row[1]}")

conn.close()
