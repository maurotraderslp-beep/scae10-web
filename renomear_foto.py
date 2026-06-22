import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:/sysflor/scae10-python/database/SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Atualizar nome do arquivo
cursor.execute("UPDATE ALUNOS SET FOTO_PATH = 'Fotos/foto_teste_aluno.png' WHERE ID = 1")
conn.commit()

print("✅ Banco atualizado: Fotos/foto_teste_aluno.png")

cursor.execute("SELECT FOTO_PATH FROM ALUNOS WHERE ID = 1")
row = cursor.fetchone()
print(f"Confirmação: {row[0]}")

conn.close()
