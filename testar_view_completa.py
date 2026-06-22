"""
Teste direto simulando a view lista_alunos
"""
import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.aluno_repository import aluno_repository

print("=" * 70)
print("  TESTANDO REPOSITORY DE ALUNOS")
print("=" * 70)
print()

# Teste 1: Contagem
print("[TESTE 1] Contagem de alunos ativos...")
try:
    count = aluno_repository.get_ativos_count()
    print(f"  Resultado: {count} alunos")
except Exception as e:
    print(f"  ERRO: {e}")
    import traceback
    traceback.print_exc()

print()

# Teste 2: Listar todos
print("[TESTE 2] Listando TODOS os alunos ativos (sem filtros)...")
try:
    alunos = aluno_repository.get_all(ativo='S')
    print(f"  Resultado: {len(alunos)} alunos retornados")
    
    if alunos:
        print(f"\n  Primeiros 5 alunos:")
        for i, aluno in enumerate(alunos[:5], 1):
            print(f"  {i}. ID={aluno.get('ID')} | NOME={aluno.get('NOME')}")
            print(f"     TURMA={aluno.get('TURMA')} | SITUACAO={aluno.get('SITUACAO')}")
            print(f"     ATIVO={aluno.get('ATIVO')} | IDADE={aluno.get('IDADE')}")
            print()
    else:
        print("\n  LISTA VAZIA!")
        
except Exception as e:
    print(f"  ERRO: {e}")
    import traceback
    traceback.print_exc()

print()

# Teste 3: Com filtro de busca
print("[TESTE 3] Buscando com filtro 'MAURO'...")
try:
    alunos = aluno_repository.get_all(ativo='S', busca='MAURO')
    print(f"  Resultado: {len(alunos)} alunos encontrados")
    if alunos:
        for i, aluno in enumerate(alunos[:3], 1):
            print(f"  {i}. {aluno.get('NOME')}")
except Exception as e:
    print(f"  ERRO: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("  FIM DOS TESTES")
print("=" * 70)
