import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Teste 1: Com parametros
print("Teste 1: Com parametros (?)")
try:
    cursor.execute("SELECT ID, NOME FROM ALUNOS WHERE ATIVO = ?", ['S'])
    rows = cursor.fetchall()
    print(f"  OK! {len(rows)} alunos")
except Exception as e:
    print(f"  ERRO: {e}")

# Teste 2: Containing com parametro
print("\nTeste 2: CONTAINING com parametro")
try:
    cursor.execute("SELECT ID, NOME FROM ALUNOS WHERE ATIVO = ? AND NOME CONTAINING ?", ['S', 'MAURO'])
    rows = cursor.fetchall()
    print(f"  OK! {len(rows)} alunos")
except Exception as e:
    print(f"  ERRO: {e}")

# Teste 3: LIKE com parametro
print("\nTeste 3: LIKE com parametro")
try:
    cursor.execute("SELECT ID, NOME FROM ALUNOS WHERE ATIVO = ? AND NOME LIKE ?", ['S', '%MAURO%'])
    rows = cursor.fetchall()
    print(f"  OK! {len(rows)} alunos")
    for row in rows[:3]:
        print(f"    {row}")
except Exception as e:
    print(f"  ERRO: {e}")

# Teste 4: Busca simples sem parametros
print("\nTeste 4: Busca direta no SQL")
try:
    cursor.execute("SELECT COUNT(*) FROM ALUNOS WHERE ATIVO = 'S'")
    count = cursor.fetchone()[0]
    print(f"  OK! {count} alunos")
except Exception as e:
    print(f"  ERRO: {e}")

conn.close()
print("\nFim dos testes")
