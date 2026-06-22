"""
Views de Solicitações
CRUD para SOLICITACOES
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from documentos.solicitacao_repository import SolicitacaoRepository


@login_required
def lista_solicitacoes(request):
    """Listar todas as solicitações"""
    status_filter = request.GET.get('status', '')
    aluno_filter = request.GET.get('aluno', '').strip()
    
    solicitacoes = SolicitacaoRepository.get_all(
        status=status_filter if status_filter else None,
        aluno_nome=aluno_filter if aluno_filter else None
    )
    
    context = {
        'solicitacoes': solicitacoes,
        'status_filter': status_filter,
        'aluno_filter': aluno_filter,
        'status_list': SolicitacaoRepository.get_status_list()
    }
    
    return render(request, 'solicitacoes/lista.html', context)


@login_required
def cadastro_solicitacao(request):
    """Cadastrar nova solicitação"""
    if request.method == 'POST':
        try:
            dados = {
                'aluno_id': int(request.POST.get('aluno_id')) if request.POST.get('aluno_id') else None,
                'tipo_documento_id': int(request.POST.get('tipo_documento_id')) if request.POST.get('tipo_documento_id') else None,
                'funcionario_id': int(request.POST.get('funcionario_id')) if request.POST.get('funcionario_id') else None,
                'status': request.POST.get('status', 'PENDENTE'),
                'certificado_numero': request.POST.get('certificado_numero', '').strip(),
                'certificado_folha': request.POST.get('certificado_folha', '').strip(),
                'certificado_livro': request.POST.get('certificado_livro', '').strip(),
                'data_emissao': request.POST.get('data_emissao') if request.POST.get('data_emissao') else None,
                'secretario_nome': request.POST.get('secretario_nome', '').strip(),
                'diretor_nome': request.POST.get('diretor_nome', '').strip(),
                'municipio': request.POST.get('municipio', '').strip(),
                'certificado_via': int(request.POST.get('certificado_via', 1)),
                'justificativa': request.POST.get('justificativa', '').strip(),
                'observacoes': request.POST.get('observacoes', '').strip()
            }
            
            # Validações
            if not dados['aluno_id']:
                messages.error(request, 'Selecione um aluno!')
                alunos = SolicitacaoRepository.get_alunos_ativos()
                tipos = SolicitacaoRepository.get_tipos_documento()
                funcionarios = SolicitacaoRepository.get_funcionarios_ativos()
                return render(request, 'solicitacoes/cadastro.html', {
                    'solicitacao': dados,
                    'alunos': alunos,
                    'tipos': tipos,
                    'funcionarios': funcionarios
                })
            
            if not dados['tipo_documento_id']:
                messages.error(request, 'Selecione um tipo de documento!')
                alunos = SolicitacaoRepository.get_alunos_ativos()
                tipos = SolicitacaoRepository.get_tipos_documento()
                funcionarios = SolicitacaoRepository.get_funcionarios_ativos()
                return render(request, 'solicitacoes/cadastro.html', {
                    'solicitacao': dados,
                    'alunos': alunos,
                    'tipos': tipos,
                    'funcionarios': funcionarios
                })
            
            if not dados['funcionario_id']:
                messages.error(request, 'Selecione um atendente!')
                alunos = SolicitacaoRepository.get_alunos_ativos()
                tipos = SolicitacaoRepository.get_tipos_documento()
                funcionarios = SolicitacaoRepository.get_funcionarios_ativos()
                return render(request, 'solicitacoes/cadastro.html', {
                    'solicitacao': dados,
                    'alunos': alunos,
                    'tipos': tipos,
                    'funcionarios': funcionarios
                })
            
            # Criar solicitação
            SolicitacaoRepository.create(dados)
            messages.success(request, 'Solicitação cadastrada com sucesso!')
            return redirect('solicitacoes:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar solicitação: {str(e)}')
    
    # GET
    alunos = SolicitacaoRepository.get_alunos_ativos()
    tipos = SolicitacaoRepository.get_tipos_documento()
    funcionarios = SolicitacaoRepository.get_funcionarios_ativos()
    
    return render(request, 'solicitacoes/cadastro.html', {
        'solicitacao': {},
        'alunos': alunos,
        'tipos': tipos,
        'funcionarios': funcionarios
    })


@login_required
def editar_solicitacao(request, solicitacao_id):
    """Editar solicitação"""
    solicitacao = SolicitacaoRepository.get_by_id(solicitacao_id)
    
    if not solicitacao:
        messages.error(request, 'Solicitação não encontrada!')
        return redirect('solicitacoes:lista')
    
    if request.method == 'POST':
        try:
            dados = {
                'aluno_id': int(request.POST.get('aluno_id')) if request.POST.get('aluno_id') else None,
                'tipo_documento_id': int(request.POST.get('tipo_documento_id')) if request.POST.get('tipo_documento_id') else None,
                'funcionario_id': int(request.POST.get('funcionario_id')) if request.POST.get('funcionario_id') else None,
                'status': request.POST.get('status', 'PENDENTE'),
                'certificado_numero': request.POST.get('certificado_numero', '').strip(),
                'certificado_folha': request.POST.get('certificado_folha', '').strip(),
                'certificado_livro': request.POST.get('certificado_livro', '').strip(),
                'data_emissao': request.POST.get('data_emissao') or None,
                'secretario_nome': request.POST.get('secretario_nome', '').strip(),
                'diretor_nome': request.POST.get('diretor_nome', '').strip(),
                'municipio': request.POST.get('municipio', '').strip(),
                'certificado_via': int(request.POST.get('certificado_via', 1)),
                'justificativa': request.POST.get('justificativa', '').strip(),
                'observacoes': request.POST.get('observacoes', '').strip(),
                'data_entrega': request.POST.get('data_entrega') or None,
                'quem_buscou': request.POST.get('quem_buscou', '').strip()
            }
            
            if not dados['aluno_id']:
                messages.error(request, 'Selecione um aluno!')
                alunos = SolicitacaoRepository.get_alunos_ativos()
                tipos = SolicitacaoRepository.get_tipos_documento()
                funcionarios = SolicitacaoRepository.get_funcionarios_ativos()
                return render(request, 'solicitacoes/cadastro.html', {
                    'solicitacao': dados,
                    'alunos': alunos,
                    'tipos': tipos,
                    'funcionarios': funcionarios,
                    'editando': True
                })
            
            SolicitacaoRepository.update(solicitacao_id, dados)
            messages.success(request, 'Solicitação atualizada com sucesso!')
            return redirect('solicitacoes:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar solicitação: {str(e)}')
    
    # GET
    alunos = SolicitacaoRepository.get_alunos_ativos()
    tipos = SolicitacaoRepository.get_tipos_documento()
    funcionarios = SolicitacaoRepository.get_funcionarios_ativos()
    
    return render(request, 'solicitacoes/cadastro.html', {
        'solicitacao': solicitacao,
        'alunos': alunos,
        'tipos': tipos,
        'funcionarios': funcionarios,
        'editando': True
    })


@login_required
def excluir_solicitacao(request, solicitacao_id):
    """Excluir solicitação"""
    try:
        SolicitacaoRepository.delete(solicitacao_id)
        messages.success(request, 'Solicitação excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir solicitação: {str(e)}')
    
    return redirect('solicitacoes:lista')
