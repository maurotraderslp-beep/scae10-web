import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:/sysflor/scae10-python/database/SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Verificar aluno ID 1
cursor.execute("SELECT ID, NOME, FOTO_PATH FROM ALUNOS WHERE ID = 1")
row = cursor.fetchone()

print(f"ANTES:")
print(f"ID: {row[0]}")
print(f"NOME: {row[1]}")
print(f"FOTO_PATH: {row[2]}")

# Atualizar para caminho relativo
novo_path = 'Fotos/foto teste aluno.png'
cursor.execute("UPDATE ALUNOS SET FOTO_PATH = ? WHERE ID = ?", [novo_path, 1])
conn.commit()

print(f"\nDEPOIS:")
print(f"FOTO_PATH: {novo_path}")

# Verificar se atualizou
cursor.execute("SELECT FOTO_PATH FROM ALUNOS WHERE ID = 1")
row = cursor.fetchone()
print(f"Confirmação: {row[0]}")

conn.close()
print("\n✅ Banco atualizado com sucesso!")
