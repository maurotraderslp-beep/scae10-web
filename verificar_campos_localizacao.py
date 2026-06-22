"""Verificar campos de localização na tabela ALUNOS"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Buscar todos os campos da tabela ALUNOS
cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ALUNOS'
    ORDER BY RDB$FIELD_POSITION
""")

rows = cursor.fetchall()

print("Campos da tabela ALUNOS relacionados a localização:")
print("-" * 60)

for row in rows:
    field_name = row[0].strip()
    if 'PRATELEIRA' in field_name or 'CORREDOR' in field_name or 'ESTANTE' in field_name:
        print(f"  ✅ {field_name}")

print("-" * 60)
print()

# Verificar se PRATELEIRA_ID existe
cursor.execute("""
    SELECT COUNT(*) 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ALUNOS' 
    AND RDB$FIELD_NAME = 'PRATELEIRA_ID'
""")

count = cursor.fetchone()[0]

if count > 0:
    print("✅ PRATELEIRA_ID EXISTE na tabela ALUNOS")
else:
    print("❌ PRATELEIRA_ID NÃO EXISTE na tabela ALUNOS")

cursor.close()
conn.close()
