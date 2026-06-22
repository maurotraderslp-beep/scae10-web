import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Buscar aluno Mauro Cabral
cursor.execute("""
    SELECT ID, NOME, FOTO_PATH 
    FROM ALUNOS 
    WHERE NOME LIKE '%Mauro Cabral%'
    ORDER BY ID
""")

rows = cursor.fetchall()

print("=" * 60)
print("ALUNOS ENCONTRADOS:")
print("=" * 60)

if rows:
    for row in rows:
        print(f"ID: {row[0]}")
        print(f"NOME: {row[1]}")
        print(f"FOTO_PATH: {row[2]}")
        print("-" * 60)
else:
    print("Nenhum aluno encontrado com 'Mauro Cabral' no nome")
    
print()
print("PRIMEIROS 5 ALUNOS:")
print("=" * 60)

cursor.execute("""
    SELECT FIRST 5 ID, NOME 
    FROM ALUNOS 
    ORDER BY ID
""")

for row in cursor.fetchall():
    print(f"ID: {row[0]} - NOME: {row[1]}")

cursor.close()
conn.close()
