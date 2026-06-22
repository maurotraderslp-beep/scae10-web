"""
Teste completo com TODOS os campos
"""
import os
import sys

sys.path.insert(0, r'c:\sysflor\scae10-web\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.aluno_repository import aluno_repository

print("=" * 70)
print("  TESTE COMPLETO - TODOS OS CAMPOS")
print("=" * 70)
print()

alunos = aluno_repository.get_all(ativo='S')
print(f"Total de alunos: {len(alunos)}")
print()

if alunos:
    aluno = alunos[0]
    print("Campos do primeiro aluno:")
    print()
    
    # Todos os campos esperados
    campos = {
        'Pessoais': ['id', 'nome', 'data_nascimento', 'telefone', 'email', 'rg', 'cpf', 'nis', 'idade'],
        'Familiares': ['nome_mae', 'nome_pai'],
        'Complementares': ['nacionalidade', 'naturalidade', 'estado_naturalidade', 'id_inep', 'cor_raca'],
        'Escolares': ['turma', 'ano_conclusao', 'situacao', 'ativo', 'modalidade_ensino', 'resolucao_autorizacao'],
        'Endereco': ['endereco', 'bairro', 'cidade', 'estado', 'zona_residencia', 'localizacao_diferenciada'],
        'Transporte': ['transporte_escolar', 'tipo_transporte', 'tipo_veiculo_transporte'],
        'Transferencia': ['escola_destino', 'inep_escola_destino', 'cidade_destino', 'uf_destino', 'contato_destino'],
        'Documentacao': ['prateleira_id'],
        'Observacoes': ['ficha_historica', 'pdc', 'comportamento', 'observacoes']
    }
    
    for categoria, chaves in campos.items():
        print(f"[{categoria}]")
        for chave in chaves:
            valor = aluno.get(chave, 'N/A')
            if valor and str(valor).strip():
                valor_str = str(valor)[:50]
            else:
                valor_str = "(vazio)"
            print(f"  {chave:30} = {valor_str}")
        print()

print("=" * 70)
