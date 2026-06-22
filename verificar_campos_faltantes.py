import fdb

conn = fdb.connect(
    dsn='localhost/3025:c:\\sysflor\\scae10-python\\database\\SCAE.FDB',
    user='SYSDBA',
    password='masterkey',
    charset='WIN1252'
)

cursor = conn.cursor()

# Campos que precisamos verificar
campos_necessarios = [
    'CORREDOR', 'ESTANTE', 'OBSERVACOES'
]

cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ALUNOS'
    ORDER BY RDB$FIELD_POSITION
""")

colunas_existentes = [row[0].strip() for row in cursor.fetchall()]

print("Verificando colunas:")
for campo in campos_necessarios:
    if campo in colunas_existentes:
        print(f"  ✅ {campo}")
    else:
        print(f"  ❌ {campo} - NÃO EXISTE")

conn.close()
