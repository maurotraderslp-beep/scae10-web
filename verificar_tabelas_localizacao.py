import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Buscar tabelas que possam ter CORREDOR, ESTANTE, PRATELEIRA
cursor.execute("""
    SELECT RDB$RELATION_NAME 
    FROM RDB$RELATIONS 
    WHERE RDB$RELATION_NAME CONTAINING 'CORREDOR' 
       OR RDB$RELATION_NAME CONTAINING 'ESTANTE'
       OR RDB$RELATION_NAME CONTAINING 'PRATELEIRA'
       OR RDB$RELATION_NAME CONTAINING 'LOCAL'
    ORDER BY RDB$RELATION_NAME
""")

print("Tabelas relacionadas a localização:")
tables = cursor.fetchall()
if tables:
    for row in tables:
        table_name = row[0].strip()
        print(f"\n  📋 {table_name}")
        
        # Ver colunas da tabela
        cursor2 = conn.cursor()
        cursor2.execute("""
            SELECT RDB$FIELD_NAME 
            FROM RDB$RELATION_FIELDS 
            WHERE RDB$RELATION_NAME = ?
            ORDER BY RDB$FIELD_POSITION
        """, [table_name])
        
        for col in cursor2.fetchall():
            print(f"      - {col[0].strip()}")
        cursor2.close()
else:
    print("  Nenhuma tabela encontrada com esses nomes")
    
    # Listar todas as tabelas do banco
    print("\n📊 Todas as tabelas do banco:")
    cursor.execute("""
        SELECT RDB$RELATION_NAME 
        FROM RDB$RELATIONS 
        WHERE RDB$SYSTEM_FLAG = 0
        ORDER BY RDB$RELATION_NAME
    """)
    
    for row in cursor.fetchall():
        print(f"  - {row[0].strip()}")

conn.close()
