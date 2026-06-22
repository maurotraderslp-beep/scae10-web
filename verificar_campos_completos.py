import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.aluno_repository import aluno_repository

alunos = aluno_repository.get_all(ativo='S')
a = alunos[0]

print("Campos carregados do primeiro aluno:")
print()

# Campos que DEVEM existir
campos_esperados = [
    'id', 'nome', 'data_nascimento', 'telefone', 'email',
    'rg', 'cpf', 'nis', 'nome_mae', 'nome_pai',
    'nacionalidade', 'naturalidade', 'estado_naturalidade', 'id_inep', 'cor_raca',
    'turma', 'ano_conclusao', 'situacao', 'ativo', 'modalidade_ensino', 'resolucao_autorizacao',
    'endereco', 'bairro', 'cidade', 'estado', 'zona_residencia', 'localizacao_diferenciada',
    'transporte_escolar', 'tipo_transporte', 'tipo_veiculo_transporte',
    'escola_destino', 'inep_escola_destino', 'cidade_destino', 'uf_destino', 'contato_destino',
    'prateleira_id', 'prateleira_descricao', 'estante_descricao', 'corredor_descricao',
    'ficha_historica', 'pdc', 'comportamento', 'observacoes',
    'foto_path'
]

for campo in sorted(campos_esperados):
    valor = a.get(campo)
    if valor:
        valor_str = str(valor)[:60]
        print(f"  ✅ {campo:35} = {valor_str}")
    else:
        print(f"  ⚪ {campo:35} = (vazio)")

print()
print(f"Total: {len([c for c in campos_esperados if a.get(c)])} campos com valor")
