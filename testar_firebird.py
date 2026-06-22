"""
Script para testar conexao com Firebird
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from documentos.aluno_repository import aluno_repository

print("=" * 60)
print("  TESTE DE CONEXAO COM FIREBIRD")
print("=" * 60)
print()

try:
    # Testar conexao
    print("[1/3] Testando conexao com Firebird...")
    count = aluno_repository.get_ativos_count()
    print(f"      OK! Alunos ativos: {count}")
    print()
    
    # Testar listagem
    print("[2/3] Buscando primeiros 5 alunos...")
    alunos = aluno_repository.get_all(ativo='S')[:5]
    
    if alunos:
        print(f"      OK! Encontrado {len(alunos)} alunos")
        print()
        for i, aluno in enumerate(alunos, 1):
            print(f"      {i}. {aluno.get('NOME', 'Sem nome')}")
            print(f"         Turma: {aluno.get('TURMA', 'N/A')}")
            print(f"         Situacao: {aluno.get('SITUACAO', 'N/A')}")
            print()
    else:
        print("      Nenhum aluno encontrado")
        print()
    
    # Testar busca
    print("[3/3] Testando busca por nome...")
    resultados = aluno_repository.get_all(busca='A')
    print(f"      OK! Busca retornou {len(resultados)} resultados")
    print()
    
    print("=" * 60)
    print("  TODOS OS TESTES PASSARAM!")
    print("=" * 60)
    
except Exception as e:
    print(f"      ERRO: {e}")
    print()
    print("=" * 60)
    print("  FALHA NO TESTE")
    print("=" * 60)
    import traceback
    traceback.print_exc()

print()
input("Pressione ENTER para sair...")
