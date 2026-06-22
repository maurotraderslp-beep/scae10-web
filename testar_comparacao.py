"""Testar filtragem em Python com dados reais do banco"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

# Valor do template
nome_modalidade = "Ensino Médio Regular"

print(f"Buscando: '{nome_modalidade}'")
print(f"Bytes: {nome_modalidade.encode('utf-8')}")
print("=" * 80)

cursor.execute("""
    SELECT ID, MODALIDADE, NUMERO_RESOLUCAO 
    FROM RESOLUCOES 
    WHERE ATIVO = 'S'
""")

rows = cursor.fetchall()

print(f"\nTotal de resoluções ativas: {len(rows)}")
print("\nTestando comparação:")

for r in rows[:5]:  # Primeiras 5
    mod_db = r[1].strip()
    match = mod_db.upper() == nome_modalidade.upper()
    
    print(f"\n  DB: '{mod_db}'")
    print(f"  DB bytes: {mod_db.encode('utf-8')}")
    print(f"  Busca: '{nome_modalidade}'")
    print(f"  Match: {match}")
    
    if match:
        print(f"  ✅ MATCH! -> {r[2]}")

cursor.close()
conn.close()
