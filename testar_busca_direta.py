"""Testar busca de resoluções com valores exatos do template"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("TESTANDO BUSCA DIRETA NO BANCO")
print("=" * 80)

# Valor exato do template
modalidade = "Ensino Médio Regular"

print(f"\nBuscando resoluções para: '{modalidade}'")
print("-" * 80)

cursor.execute("""
    SELECT ID, NUMERO_RESOLUCAO, DESCRICAO 
    FROM RESOLUCOES 
    WHERE MODALIDADE = ? AND ATIVO = 'S'
    ORDER BY NUMERO_RESOLUCAO
""", [modalidade])

rows = cursor.fetchall()

print(f"Encontradas {len(rows)} resoluções:")
for row in rows:
    print(f"  ID={row[0]}, NUMERO={row[1]}, DESC={row[2]}")

print("\n" + "=" * 80)
print("TODAS AS RESOLUCOES COM MODALIDADE E ATIVO:")
print("=" * 80)

cursor.execute("""
    SELECT ID, MODALIDADE, NUMERO_RESOLUCAO, ATIVO
    FROM RESOLUCOES
    ORDER BY MODALIDADE, NUMERO_RESOLUCAO
""")

rows = cursor.fetchall()

for row in rows[:20]:  # Primeiras 20
    print(f"  ID={row[0]}, MOD='{row[1]}', NUM='{row[2]}', ATIVO='{row[3]}'")

cursor.close()
conn.close()
