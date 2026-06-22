import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.aluno_repository import aluno_repository

alunos = aluno_repository.get_all(ativo='S')
a = alunos[0]

print("=" * 80)
print("  TESTE - CAMPOS DE DOCUMENTAÇÃO")
print("=" * 80)
print()

docs = [
    'doc_foto3x4', 'doc_historico', 'doc_certificado', 'doc_rg',
    'doc_cpf', 'doc_comprovante_residencia', 'doc_certidao_nascimento',
    'doc_cartao_sus', 'doc_folha_resumo', 'doc_carteira_vacina'
]

print(f"Aluno: {a.get('nome')}")
print()

for doc in docs:
    valor = a.get(doc)
    if valor == 'S':
        print(f"  ✅ {doc:35} = ENTREGUE")
    else:
        print(f"  ⚪ {doc:35} = Pendente")

print()
print("=" * 80)
