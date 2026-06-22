"""
Teste de conversão de foto path
"""
import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.file_utils import converter_foto_path
from documentos.aluno_repository import aluno_repository

print("=" * 80)
print("  TESTE DE CONVERSÃO DE FOTO")
print("=" * 80)
print()

# Buscar primeiro aluno com foto
alunos = aluno_repository.get_all(ativo='S')

alunos_com_foto = [a for a in alunos if a.get('foto_path')]
alunos_sem_foto = [a for a in alunos if not a.get('foto_path')]

print(f"Total de alunos: {len(alunos)}")
print(f"Alunos com foto_path: {len(alunos_com_foto)}")
print(f"Alunos sem foto_path: {len(alunos_sem_foto)}")
print()

if alunos_com_foto:
    print("-" * 80)
    print("TESTANDO ALUNOS COM FOTO:")
    print("-" * 80)
    
    for aluno in alunos_com_foto[:3]:  # Testar primeiros 3
        print(f"\nAluno: {aluno.get('nome')}")
        print(f"  foto_path (banco): {aluno.get('foto_path')}")
        
        url = converter_foto_path(aluno.get('foto_path'))
        print(f"  foto_url (web):    {url}")
        
        if url:
            print(f"  ✅ Conversão OK")
        else:
            print(f"  ❌ Erro na conversão")

print()
print("-" * 80)
print("TESTANDO ALUNO SEM FOTO:")
print("-" * 80)

if alunos_sem_foto:
    aluno = alunos_sem_foto[0]
    print(f"\nAluno: {aluno.get('nome')}")
    print(f"  foto_path (banco): (vazio)")
    
    url = converter_foto_path(None)
    print(f"  foto_url (web):    {url}")
    
    if url is None:
        print(f"  ✅ Retorna None corretamente")
    else:
        print(f"  ❌ Deveria retornar None")

print()
print("=" * 80)
print("  TESTE CONCLUÍDO")
print("=" * 80)
