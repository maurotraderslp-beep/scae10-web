"""
Teste com Corredor, Estante e Prateleira
"""
import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.aluno_repository import aluno_repository, localizacao_repository

print("=" * 70)
print("  TESTE - CORREDOR, ESTANTE E PRATELEIRA")
print("=" * 70)
print()

# Testar corredores
print("[1] Corredores:")
corredores = localizacao_repository.get_corredores()
print(f"  Total: {len(corredores)}")
for c in corredores[:3]:
    print(f"    - ID={c['id']} | {c['descricao']}")
print()

# Testar estantes
print("[2] Estantes:")
estantes = localizacao_repository.get_estantes()
print(f"  Total: {len(estantes)}")
for e in estantes[:3]:
    print(f"    - ID={e['id']} | {e['descricao']} | Corredor ID={e['corredor_id']}")
print()

# Testar prateleiras
print("[3] Prateleiras:")
prateleiras = localizacao_repository.get_prateleiras()
print(f"  Total: {len(prateleiras)}")
for p in prateleiras[:3]:
    print(f"    - ID={p['id']} | {p['descricao']} | Estante ID={p['estante_id']}")
print()

# Testar aluno com localização
print("[4] Aluno com localização:")
alunos = aluno_repository.get_all(ativo='S')
if alunos:
    # Buscar primeiro aluno com prateleira
    aluno_com_local = None
    for a in alunos:
        if a.get('prateleira_id'):
            aluno_com_local = a
            break
    
    if aluno_com_local:
        print(f"  Nome: {aluno_com_local['nome']}")
        print(f"  Prateleira ID: {aluno_com_local['prateleira_id']}")
        print(f"  Prateleira: {aluno_com_local.get('prateleira_descricao', 'N/A')}")
        print(f"  Estante: {aluno_com_local.get('estante_descricao', 'N/A')}")
        print(f"  Corredor: {aluno_com_local.get('corredor_descricao', 'N/A')}")
    else:
        print("  Nenhum aluno com prateleira encontrada")

print()
print("=" * 70)
