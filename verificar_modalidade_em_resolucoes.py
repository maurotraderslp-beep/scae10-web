"""Verificar valores do campo MODALIDADE na tabela RESOLUCOES"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("VALORES DO CAMPO MODALIDADE NA TABELA RESOLUCOES")
print("=" * 80)

cursor.execute("""
    SELECT DISTINCT MODALIDADE 
    FROM RESOLUCOES 
    WHERE ATIVO = 'S'
    ORDER BY MODALIDADE
""")

rows = cursor.fetchall()

print(f"\nModalidades encontradas em RESOLUCOES ({len(rows)}):")
for i, row in enumerate(rows, 1):
    modalidade = row[0].strip() if row[0] else 'NULL'
    print(f"  {i}. '{modalidade}'")

print("\n" + "=" * 80)

cursor.close()
conn.close()
