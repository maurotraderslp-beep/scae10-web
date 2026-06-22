"""Verificar histórico de alterações do aluno 4"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("VERIFICANDO TODOS OS CAMPOS DO ALUNO 4")
print("=" * 80)
print()

# Buscar TODAS as colunas
cursor.execute("""
    SELECT * FROM ALUNOS WHERE ID = 4
""")

row = cursor.fetchone()
columns = [desc[0] for desc in cursor.description]

print("Campos do aluno 4:")
print("-" * 80)

for col, val in zip(columns, row):
    if val is not None and val != '':
        print(f"  ✅ {col}: {val}")
    else:
        print(f"  ❌ {col}: (vazio)")

print("-" * 80)
print()

# Contar preenchidos vs vazios
preenchidos = sum(1 for val in row if val is not None and val != '')
vazios = sum(1 for val in row if val is None or val == '')

print(f"Total de campos: {len(columns)}")
print(f"Preenchidos: {preenchidos}")
print(f"Vazios: {vazios}")
print()

print("=" * 80)
print("DATA_ALTERACAO:", [val for col, val in zip(columns, row) if col == 'DATA_ALTERACAO'][0])
print("=" * 80)

cursor.close()
conn.close()
