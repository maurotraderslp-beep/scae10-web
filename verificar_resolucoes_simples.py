"""Verificar resolucoes por modalidade"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.firebird_service import firebird_service

conn = firebird_service.get_connection()
cursor = conn.cursor()

print("=" * 80)
print("RESOLUCOES POR MODALIDADE")
print("=" * 80)

# Buscar todas as resolucoes
cursor.execute("""
    SELECT ID, MODALIDADE, NUMERO_RESOLUCAO, DESCRICAO
    FROM RESOLUCOES
    WHERE ATIVO = 'S'
    ORDER BY MODALIDADE, NUMERO_RESOLUCAO
""")

dados = cursor.fetchall()

print(f"\nTotal de resolucoes ativas: {len(dados)}")
print("\nAgrupadas por MODALIDADE_ID:")

from collections import defaultdict
resolucoes_por_modalidade = defaultdict(list)

for dado in dados:
    id_resolucao = dado[0]
    id_modalidade = dado[1]
    numero = str(dado[2]).strip() if dado[2] else ''
    descricao = str(dado[3]).strip() if dado[3] else ''
    
    resolucoes_por_modalidade[id_modalidade].append({
        'id': id_resolucao,
        'numero': numero,
        'descricao': descricao
    })

for modalidade_id in sorted(resolucoes_por_modalidade.keys()):
    resolucoes = resolucoes_por_modalidade[modalidade_id]
    print(f"\n  MODALIDADE_ID = {modalidade_id} ({len(resolucoes)} resolucoes):")
    for res in resolucoes:
        print(f"    [{res['id']}] {res['numero']}")

cursor.close()
conn.close()
