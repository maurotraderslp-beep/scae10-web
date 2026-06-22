"""
Views de Alunos
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from documentos.aluno_repository import aluno_repository, localizacao_repository
from documentos.file_utils import converter_foto_path


@login_required
def lista_alunos(request):
    """Listagem de todos os alunos ativos"""
    
    # Busca parâmetros de busca
    busca = request.GET.get('busca', '')
    turma = request.GET.get('turma', '')
    situacao = request.GET.get('situacao', '')
    
    print(f"\n=== LISTA ALUNOS ===")
    print(f"Busca: {busca}, Turma: {turma}, Situacao: {situacao}")
    
    # Buscar alunos do Firebird
    try:
        alunos = aluno_repository.get_all(
            ativo='S',
            busca=busca,
            turma=turma,
            situacao=situacao
        )
        print(f"Retornou {len(alunos)} alunos")
        if alunos:
            print(f"Primeiro aluno: {alunos[0].get('nome')}")
            # Debug: mostrar primeiros 3 alunos
            for i, aluno in enumerate(alunos[:3]):
                print(f"  Aluno[{i}]: id={aluno.get('id')}, nome='{aluno.get('nome')}'")
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        alunos = []
        messages.error(request, f'Erro ao carregar alunos: {e}')
    
    context = {
        'alunos': alunos,
        'busca': busca,
        'turma': turma,
        'situacao': situacao,
    }
    
    return render(request, 'alunos/lista.html', context)


@login_required
def detalhe_aluno(request, aluno_id):
    """Detalhes de um aluno específico"""
    try:
        aluno = aluno_repository.get_by_id(aluno_id)
    except Exception as e:
        aluno = None
        messages.error(request, f'Erro ao carregar aluno: {e}')
    
    if not aluno:
        messages.error(request, 'Aluno não encontrado.')
        return redirect('alunos:lista')
    
    # Converter caminho da foto para URL web
    foto_url = converter_foto_path(aluno.get('foto_path'))
    
    context = {
        'aluno': aluno,
        'foto_url': foto_url,
    }
    
    return render(request, 'alunos/detalhe.html', context)


@login_required
def cadastro_aluno(request):
    """Cadastro de novo aluno"""
    
    # Carregar listas para selects
    context = {
        'corredores': localizacao_repository.get_corredores(),
        'estantes': localizacao_repository.get_estantes(),
        'prateleiras': localizacao_repository.get_prateleiras(),
    }
    
    if request.method == 'POST':
        # TODO: Implementar criação
        messages.info(request, 'Cadastro será implementado em breve.')
        return redirect('alunos:lista')
    
    return render(request, 'alunos/cadastro.html', context)


@login_required
def editar_aluno(request, aluno_id):
    """Edição de aluno existente"""
    try:
        aluno = aluno_repository.get_by_id(aluno_id)
    except Exception as e:
        aluno = None
        messages.error(request, f'Erro ao carregar aluno: {e}')
    
    if not aluno:
        messages.error(request, 'Aluno não encontrado.')
        return redirect('alunos:lista')
    
    # Converter caminho da foto para URL web
    foto_url = converter_foto_path(aluno.get('foto_path'))
    
    # DEBUG: Verificar valores
    print(f"[DEBUG EDITAR] Aluno ID: {aluno.get('id')}")
    print(f"[DEBUG EDITAR] foto_path no banco: '{aluno.get('foto_path')}'")
    print(f"[DEBUG EDITAR] foto_url convertida: '{foto_url}'")
    print(f"[DEBUG EDITAR] editando: True")
    
    # Lista de UFs para selects
    ufs = ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    
    # Carregar listas para selects
    corredores = localizacao_repository.get_corredores()
    estantes = localizacao_repository.get_estantes()
    prateleiras = localizacao_repository.get_prateleiras()
    
    # Converter para JSON para o JavaScript
    import json
    estantes_json = json.dumps([{  
        'id': e['id'], 
        'descricao': e['descricao'], 
        'corredor_id': e['corredor_id']
    } for e in estantes])
    
    prateleiras_json = json.dumps([{  
        'id': p['id'], 
        'descricao': p['descricao'], 
        'estante_id': p['estante_id']
    } for p in prateleiras])
    
    context = {
        'aluno': aluno,
        'editando': True,
        'foto_url': foto_url,
        'ufs': ufs,
        'corredores': corredores,
        'estantes': estantes,
        'prateleiras': prateleiras,
        'estantes_json': estantes_json,
        'prateleiras_json': prateleiras_json,
    }
    
    if request.method == 'POST':
        try:
            # DEBUG: Verificar o que está sendo enviado
            print("=" * 80)
            print("[DEBUG POST] Dados recebidos do formulário:")
            print(f"[DEBUG POST] transporte_escolar = '{request.POST.get('transporte_escolar')}'")
            print(f"[DEBUG POST] tipo_transporte = '{request.POST.get('tipo_transporte')}'")
            print(f"[DEBUG POST] prateleira_id = '{request.POST.get('prateleira_id')}'")
            print(f"[DEBUG POST] FILES = {request.FILES}")
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                print(f"[DEBUG POST] FOTO RECEBIDA: name={foto.name}, size={foto.size}, content_type={foto.content_type}")
            else:
                print("[DEBUG POST] NENHUMA FOTO FOI SELECIONADA!")
            print("=" * 80)
            
            # Processar upload de foto
            foto_path_atual = aluno.get('foto_path', '')
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                # Criar pasta se não existir
                import os
                from django.conf import settings
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'Fotos')
                os.makedirs(fotos_dir, exist_ok=True)
                
                # Salvar foto
                nome_arquivo = foto.name
                # Remover espaços e caracteres especiais do nome
                import unicodedata
                nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
                nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode('ASCII')
                nome_arquivo = nome_arquivo.replace(' ', '_')
                
                caminho_completo = os.path.join(fotos_dir, nome_arquivo)
                
                with open(caminho_completo, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                # Atualizar path no banco (salvar caminho relativo)
                foto_path_atual = f'Fotos/{nome_arquivo}'
                print(f"[DEBUG] Foto salva em: {caminho_completo}")
                print(f"[DEBUG] Path no banco: {foto_path_atual}")
            
            # CORREÇÃO CRÍTICA: UPDATE PARCIAL para não apagar dados existentes!
            # Só atualizar campos que foram enviados no POST
            dados_aluno = {}
            
            # Lista de todos os campos possíveis (exceto foto_path que já foi tratado)
            campos_possiveis = [
                'nome', 'data_nascimento', 'nome_mae', 'nome_pai', 
                'telefone', 'email', 'rg', 'cpf', 'nis',
                'nacionalidade', 'naturalidade', 'estado_naturalidade',
                'id_inep', 'cor_raca', 'turma', 'ano_conclusao', 'situacao',
                'modalidade_ensino', 'resolucao_autorizacao',
                'endereco', 'bairro', 'cidade', 'estado',
                'zona_residencia', 'localizacao_diferenciada',
                'transporte_escolar', 'tipo_transporte', 'tipo_veiculo_transporte',
                'escola_destino', 'inep_escola_destino', 'cidade_destino',
                'uf_destino', 'contato_destino',
                'prateleira_id', 'ficha_historica', 'pdc',
                'comportamento', 'observacoes',
            ]
            
            # Adicionar só campos que foram enviados
            for campo in campos_possiveis:
                valor = request.POST.get(campo)
                # Só incluir se veio no POST (mesmo que seja vazio)
                if request.POST.get(campo) is not None:
                    # Converter vazio para None
                    dados_aluno[campo] = valor if valor else None
            
            # Campos de documentação (checkboxes - sempre enviar S ou N)
            doc_campos = [
                'doc_foto3x4', 'doc_historico', 'doc_certificado', 'doc_rg',
                'doc_cpf', 'doc_comprovante_residencia', 'doc_certidao_nascimento',
                'doc_cartao_sus', 'doc_folha_resumo', 'doc_carteira_vacina',
            ]
            
            for doc_campo in doc_campos:
                # Checkbox só vem no POST se estiver marcado
                if request.POST.get(doc_campo) is not None:
                    dados_aluno[doc_campo] = 'S' if request.POST.get(doc_campo) else 'N'
            
            # Adicionar foto_path se houve upload
            if foto_path_atual != aluno.get('foto_path', ''):
                dados_aluno['foto_path'] = foto_path_atual
            
            print(f"[UPDATE PARCIAL] Campos a atualizar: {list(dados_aluno.keys())}")
            
            # Atualizar no Firebird
            aluno_repository.update(aluno_id, dados_aluno)
            
            messages.success(request, f'Aluno "{dados_aluno["nome"]}" atualizado com sucesso!')
            return redirect('alunos:detalhe', aluno_id=aluno_id)
            
        except Exception as e:
            messages.error(request, f'Erro ao salvar aluno: {e}')
            import traceback
            traceback.print_exc()
    
    return render(request, 'alunos/cadastro.html', context)


@login_required
def testar_foto(request):
    """Página de teste para verificar se fotos estão sendo servidas"""
    return render(request, 'alunos/testar_foto.html')


@login_required
def teste_upload(request):
    """Página de teste simples para upload"""
    return render(request, 'alunos/teste_upload.html')


@login_required
def excluir_aluno(request, aluno_id):
    """Excluir aluno (desativa e redireciona)"""
    try:
        # Só desativa em vez de apagar fisicamente
        aluno_repository.update(aluno_id, {'ativo': 'N'})
        messages.success(request, f'Aluno excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir aluno: {e}')
    
    return redirect('alunos:lista')


@login_required
def buscar_resolucoes_por_modalidade(request):
    """API AJAX: Buscar resoluções filtradas por modalidade"""
    from django.http import JsonResponse
    
    nome_modalidade = request.GET.get('modalidade', '')
    
    print(f"[DEBUG API] Modalidade recebida: '{nome_modalidade}'")
    print(f"[DEBUG API] Tipo: {type(nome_modalidade)}")
    print(f"[DEBUG API] Bytes: {nome_modalidade.encode('utf-8')}")
    
    if not nome_modalidade:
        return JsonResponse({'error': 'Modalidade não informada'}, status=400)
    
    try:
        # Buscar TODAS as resoluções e filtrar em Python (problema de encoding)
        from documentos.firebird_service import firebird_service
        
        conn = firebird_service.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ID, MODALIDADE, NUMERO_RESOLUCAO, DESCRICAO 
            FROM RESOLUCOES 
            WHERE ATIVO = 'S'
            ORDER BY NUMERO_RESOLUCAO
        """)
        
        todas_resolucoes = cursor.fetchall()
        
        # Filtrar em Python comparando strings normalizadas
        resolucoes_filtradas = []
        print(f"[DEBUG API] Total de resoluções ativas: {len(todas_resolucoes)}")
        
        for r in todas_resolucoes:
            modalidade_db = r[1].strip() if r[1] else ''
            
            # Corrigir double-encoding do Firebird
            try:
                # Tenta decodificar como latin-1 e re-codificar como UTF-8
                modalidade_corrigida = modalidade_db.encode('latin-1').decode('utf-8')
            except:
                # Se falhar, usa original
                modalidade_corrigida = modalidade_db
            
            # Debug: mostrar comparações
            match = modalidade_corrigida.upper() == nome_modalidade.upper()
            if match:
                print(f"[DEBUG API] ✅ MATCH: DB='{modalidade_corrigida}' | TEMPLATE='{nome_modalidade}'")
            
            # Comparação case-insensitive
            if match:
                resolucoes_filtradas.append({
                    'id': r[0],
                    'numero_resolucao': r[2],
                    'descricao': r[3] if r[3] else ''
                })
        
        # Se não encontrou, mostrar todas as modalidades diferentes
        if len(resolucoes_filtradas) == 0:
            print(f"[DEBUG API] ❌ Nenhum match encontrado!")
            print(f"[DEBUG API] Buscado: '{nome_modalidade}'")
            modalidades_unicas = set()
            for r in todas_resolucoes:
                if r[1]:
                    modalidades_unicas.add(r[1].strip())
            print(f"[DEBUG API] Modalidades disponíveis no banco:")
            for m in sorted(modalidades_unicas):
                print(f"  - '{m}'")
        
        print(f"[DEBUG API] Encontradas {len(resolucoes_filtradas)} resoluções")
        
        cursor.close()
        conn.close()
        
        return JsonResponse({
            'success': True,
            'resolucoes': resolucoes_filtradas
        })
    except Exception as e:
        print(f"[DEBUG API] ERRO: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
