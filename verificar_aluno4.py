"""Verificar dados do aluno ID 4"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Buscar todos os dados do aluno 4
cursor.execute("""
    SELECT * FROM ALUNOS WHERE ID = 4
""")

row = cursor.fetchone()
columns = [desc[0] for desc in cursor.description]

print("=" * 80)
print("DADOS DO ALUNO ID 4")
print("=" * 80)

for col, val in zip(columns, row):
    if val is not None and val != '':
        print(f"{col}: {val}")

print("=" * 80)

cursor.close()
conn.close()
