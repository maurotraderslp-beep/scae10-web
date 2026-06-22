"""Verificar estrutura da tabela MODALIDADES"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("ESTRUTURA DA TABELA MODALIDADES")
print("=" * 80)

# Buscar campos da tabela MODALIDADES
cursor.execute("""
    SELECT RDB$FIELD_NAME 
    FROM RDB$RELATION_FIELDS 
    WHERE RDB$RELATION_NAME = 'MODALIDADES'
    ORDER BY RDB$FIELD_POSITION
""")

campos = cursor.fetchall()

print("\nCampos da tabela MODALIDADES:")
for campo in campos:
    print(f"  - {campo[0].strip()}")

# Buscar todos os dados da tabela MODALIDADES
cursor.execute("""
    SELECT * FROM MODALIDADES ORDER BY DESCRICAO
""")

dados = cursor.fetchall()

print(f"\n\nDados na tabela MODALIDADES ({len(dados)} registros):")
for dado in dados:
    print(f"\n  ID: {dado[0]}")
    for i, campo in enumerate(campos):
        if i > 0:  # Pular ID
            valor = str(dado[i]).strip() if dado[i] else 'NULL'
            print(f"    {campo[0].strip()}: {valor}")

cursor.close()
conn.close()
