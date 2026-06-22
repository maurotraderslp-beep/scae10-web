import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Teste: Query completa sem filtros (como o repository faz)
print("Teste: Query completa sem filtro de busca")
query = """
    SELECT 
        ID, NOME, DATA_NASCIMENTO, NOME_MAE,
        TURMA, SITUACAO, ATIVO
    FROM ALUNOS
    WHERE 1=1
    AND ATIVO = ?
    ORDER BY NOME
"""

try:
    cursor.execute(query, ['S'])
    rows = cursor.fetchall()
    print(f"  OK! {len(rows)} alunos retornados")
    if rows:
        print(f"  Primeiro: {rows[0][1]}")
        print(f"  Último: {rows[-1][1]}")
except Exception as e:
    print(f"  ERRO: {e}")
    import traceback
    traceback.print_exc()

conn.close()
