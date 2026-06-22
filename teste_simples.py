import fdb

try:
    print("Testando conexao com Firebird 2.5 (porta 3025)...")
    conn = fdb.connect(
        dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
        user='SYSDBA',
        password='masterkey',
        charset='WIN1252'
    )
    print("CONECTADO!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ALUNOS")
    count = cursor.fetchone()[0]
    print(f"Total de alunos: {count}")
    
    cursor.execute("SELECT ID, NOME, TURMA FROM ALUNOS ROWS 5")
    print("\nPrimeiros 5 alunos:")
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]} (Turma: {row[2]})")
    
    conn.close()
    print("\nTeste OK!")
    
except Exception as e:
    print(f"ERRO: {e}")
