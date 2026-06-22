import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:/sysflor/scae10-python/database/SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Buscar constraints da tabela ALUNOS
print("=" * 80)
print("CONSTRAINTS DA TABELA ALUNOS")
print("=" * 80)

query = """
    SELECT 
        rc.RDB$CONSTRAINT_NAME,
        rc.RDB$INDEX_NAME,
        t.RDB$TRIGGER_SOURCE
    FROM RDB$RELATION_CONSTRAINTS rc
    LEFT JOIN RDB$CHECK_CONSTRAINTS cc ON rc.RDB$CONSTRAINT_NAME = cc.RDB$CONSTRAINT_NAME
    LEFT JOIN RDB$TRIGGERS t ON cc.RDB$TRIGGER_NAME = t.RDB$TRIGGER_NAME
    WHERE rc.RDB$RELATION_NAME = 'ALUNOS'
    AND rc.RDB$CONSTRAINT_TYPE = 'CHECK'
"""

cursor.execute(query)
results = cursor.fetchall()

for row in results:
    constraint_name = row[0].strip() if row[0] else 'N/A'
    trigger_name = row[1].strip() if row[1] else 'N/A'
    trigger_source = row[2].strip() if row[2] else 'N/A'
    
    print(f"\nConstraint: {constraint_name}")
    print(f"Trigger: {trigger_name}")
    print(f"Definição: {trigger_source[:200]}...")
    print("-" * 80)

conn.close()

print("\n✅ Consulta finalizada!")
