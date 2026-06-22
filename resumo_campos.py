"""
Resumo completo dos campos implementados
"""
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
print("  RESUMO COMPLETO - CAMPOS DO FORMULÁRIO DE ALUNOS")
print("=" * 80)
print()

# Organização por abas
abas = {
    'ABA 1 - DADOS DO ALUNO': {
        'Dados Pessoais': ['nome', 'data_nascimento', 'telefone', 'email', 'rg', 'cpf', 'nis'],
        'Dados Familiares': ['nome_mae', 'nome_pai'],
        'Dados Complementares': ['nacionalidade', 'naturalidade', 'estado_naturalidade', 'id_inep', 'cor_raca'],
        'Dados Escolares': ['turma', 'ano_conclusao', 'situacao', 'modalidade_ensino', 'resolucao_autorizacao'],
        'Localização Documentação': ['prateleira_id', 'prateleira_descricao', 'estante_descricao', 'corredor_descricao'],
        'Foto': ['foto_path']
    },
    'ABA 2 - ENDEREÇO': {
        'Endereço Residencial': ['endereco', 'bairro', 'cidade', 'estado', 'zona_residencia', 'localizacao_diferenciada']
    },
    'ABA 3 - TRANSPORTE ESCOLAR': {
        'Transporte': ['transporte_escolar', 'tipo_transporte', 'tipo_veiculo_transporte']
    },
    'ABA 4 - TRANSFERÊNCIA': {
        'Escola Destino': ['escola_destino', 'inep_escola_destino', 'cidade_destino', 'uf_destino', 'contato_destino']
    },
    'ABA 5 - OBSERVAÇÕES': {
        'Observações': ['ficha_historica', 'pdc', 'comportamento', 'observacoes']
    }
}

total_campos = 0
total_com_valor = 0

for aba, secoes in abas.items():
    print(f"\n{aba}")
    print("-" * 80)
    
    for secao, campos in secoes.items():
        print(f"\n  📋 {secao}:")
        for campo in campos:
            total_campos += 1
            valor = a.get(campo)
            if valor:
                total_com_valor += 1
                valor_str = str(valor)[:50]
                print(f"    ✅ {campo:30} = {valor_str}")
            else:
                print(f"    ⚪ {campo:30} = (vazio)")

print()
print("=" * 80)
print(f"  TOTAL: {total_com_valor}/{total_campos} campos com valor")
print("=" * 80)
