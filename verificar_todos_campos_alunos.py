"""Verificar TODOS os campos da tabela ALUNOS"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Buscar TODOS os campos da tabela ALUNOS
cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ALUNOS'
    ORDER BY RDB$FIELD_POSITION
""")

rows = cursor.fetchall()

print("=" * 80)
print("TODOS OS CAMPOS DA TABELA ALUNOS:")
print("=" * 80)

for i, row in enumerate(rows, 1):
    field_name = row[0].strip()
    print(f"{i:3}. {field_name}")

print("=" * 80)
print(f"\nTotal de campos: {len(rows)}")

# Verificar se existem os campos de localização
print("\n" + "=" * 80)
print("VERIFICANDO CAMPOS DE LOCALIZAÇÃO:")
print("=" * 80)

campos_localizacao = ['CORREDOR_ID', 'ESTANTE_ID', 'PRATELEIRA_ID']
for campo in campos_localizacao:
    encontrado = any(row[0].strip() == campo for row in rows)
    if encontrado:
        print(f"  ✅ {campo} - EXISTE")
    else:
        print(f"  ❌ {campo} - NÃO EXISTE")

print("=" * 80)

# Agora verificar se há ALGUM campo com CORREDOR, ESTANTE ou PRATELEIRA
print("\nCampos relacionados à localização:")
for row in rows:
    field_name = row[0].strip()
    if 'CORREDOR' in field_name or 'ESTANTE' in field_name or 'PRATELEIRA' in field_name:
        print(f"  📍 {field_name}")

cursor.close()
conn.close()
