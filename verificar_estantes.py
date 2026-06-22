"""Verificar estrutura da tabela ESTANTES"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Verificar campos
cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'ESTANTES' 
    ORDER BY RDB$FIELD_POSITION
""")

fields = cursor.fetchall()

print("=" * 80)
print("ESTRUTURA DA TABELA ESTANTES")
print("=" * 80)
print("\nCampos:")
for f in fields:
    print(f"  - {f[0].strip()}")

# Verificar dados existentes
cursor.execute("SELECT COUNT(*) FROM ESTANTES")
count = cursor.fetchone()[0]
print(f"\nTotal de registros: {count}")

if count > 0:
    cursor.execute("SELECT * FROM ESTANTES")
    rows = cursor.fetchall()
    print(f"\nPrimeiros 5 registros:")
    for row in rows[:5]:
        print(f"  {row}")

cursor.close()
conn.close()
