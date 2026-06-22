"""
Teste final com chaves minúsculas
"""
import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.aluno_repository import aluno_repository

print("=" * 70)
print("  TESTE FINAL - Chaves Minúsculas")
print("=" * 70)
print()

# Testar listagem
alunos = aluno_repository.get_all(ativo='S')
print(f"Total de alunos: {len(alunos)}")
print()

if alunos:
    print("Primeiro aluno:")
    aluno = alunos[0]
    print(f"  ID (chave 'id'): {aluno.get('id')}")
    print(f"  Nome (chave 'nome'): {aluno.get('nome')}")
    print(f"  Turma (chave 'turma'): {aluno.get('turma')}")
    print(f"  Situacao (chave 'situacao'): {aluno.get('situacao')}")
    print(f"  Ativo (chave 'ativo'): {aluno.get('ativo')}")
    print(f"  Idade (chave 'idade'): {aluno.get('idade')}")
    print(f"  Data Nascimento (chave 'data_nascimento'): {aluno.get('data_nascimento')}")
    print()
    
    # Verificar se todas as chaves esperadas existem
    chaves_esperadas = ['id', 'nome', 'data_nascimento', 'nome_mae', 'turma', 'situacao', 'ativo', 'cpf', 'rg', 'naturalidade', 'estado_naturalidade', 'cor_raca', 'nis', 'idade']
    chaves_presentes = list(aluno.keys())
    
    print("Verificação de chaves:")
    for chave in chaves_esperadas:
        status = "✅" if chave in chaves_presentes else "❌"
        print(f"  {status} {chave}")

print()
print("=" * 70)
