from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from documentos.prateleira_repository import PrateleiraRepository
from documentos.estante_repository import EstanteRepository


@login_required
def lista_prateleiras(request):
    """Listar todas as prateleiras"""
    try:
        prateleiras = PrateleiraRepository.get_all()
    except Exception as e:
        messages.error(request, f'Erro ao carregar prateleiras: {e}')
        prateleiras = []
    
    return render(request, 'prateleiras/lista.html', {
        'prateleiras': prateleiras
    })


@login_required
def cadastro_prateleira(request):
    """Cadastrar nova prateleira"""
    if request.method == 'POST':
        try:
            foto_path = ''
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                import os
                from django.conf import settings
                
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'prateleiras')
                os.makedirs(fotos_dir, exist_ok=True)
                
                import unicodedata
                nome_arquivo = foto.name
                nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
                nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode('ASCII')
                nome_arquivo = nome_arquivo.replace(' ', '_')
                
                caminho_completo = os.path.join(fotos_dir, nome_arquivo)
                
                with open(caminho_completo, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                foto_path = f'prateleiras/{nome_arquivo}'
            
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'estante_id': int(request.POST.get('estante_id')) if request.POST.get('estante_id') else None,
                'foto_path': foto_path,
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Código é obrigatório!')
                estantes = EstanteRepository.get_all()
                return render(request, 'prateleiras/cadastro.html', {'prateleira': dados, 'estantes': estantes})
            
            if not dados['descricao']:
                messages.error(request, 'Descrição é obrigatória!')
                estantes = EstanteRepository.get_all()
                return render(request, 'prateleiras/cadastro.html', {'prateleira': dados, 'estantes': estantes})
            
            if not dados['estante_id']:
                messages.error(request, 'Selecione uma estante!')
                estantes = EstanteRepository.get_all()
                return render(request, 'prateleiras/cadastro.html', {'prateleira': dados, 'estantes': estantes})
            
            PrateleiraRepository.create(dados)
            messages.success(request, f'Prateleira "{dados["descricao"]}" cadastrada com sucesso!')
            return redirect('prateleiras:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar prateleira: {e}')
    
    # GET - carregar estantes para o select
    try:
        estantes = EstanteRepository.get_all()
    except:
        estantes = []
    
    return render(request, 'prateleiras/cadastro.html', {
        'prateleira': {},
        'estantes': estantes
    })


@login_required
def editar_prateleira(request, prateleira_id):
    """Editar prateleira existente"""
    try:
        prateleira = PrateleiraRepository.get_by_id(prateleira_id)
        
        if not prateleira:
            messages.error(request, 'Prateleira não encontrada!')
            return redirect('prateleiras:lista')
        
        if request.method == 'POST':
            foto_path = prateleira.get('foto_path', '')
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                import os
                from django.conf import settings
                
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'prateleiras')
                os.makedirs(fotos_dir, exist_ok=True)
                
                import unicodedata
                nome_arquivo = foto.name
                nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
                nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode('ASCII')
                nome_arquivo = nome_arquivo.replace(' ', '_')
                
                caminho_completo = os.path.join(fotos_dir, nome_arquivo)
                
                with open(caminho_completo, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                foto_path = f'prateleiras/{nome_arquivo}'
            
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'estante_id': int(request.POST.get('estante_id')) if request.POST.get('estante_id') else None,
                'foto_path': foto_path,
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Código é obrigatório!')
                estantes = EstanteRepository.get_all()
                return render(request, 'prateleiras/cadastro.html', {'prateleira': {**prateleira, **dados}, 'estantes': estantes})
            
            if not dados['descricao']:
                messages.error(request, 'Descrição é obrigatória!')
                estantes = EstanteRepository.get_all()
                return render(request, 'prateleiras/cadastro.html', {'prateleira': {**prateleira, **dados}, 'estantes': estantes})
            
            if not dados['estante_id']:
                messages.error(request, 'Selecione uma estante!')
                estantes = EstanteRepository.get_all()
                return render(request, 'prateleiras/cadastro.html', {'prateleira': {**prateleira, **dados}, 'estantes': estantes})
            
            PrateleiraRepository.update(prateleira_id, dados)
            messages.success(request, f'Prateleira "{dados["descricao"]}" atualizada com sucesso!')
            return redirect('prateleiras:lista')
        
        # GET - carregar estantes para o select
        try:
            estantes = EstanteRepository.get_all()
        except:
            estantes = []
        
        return render(request, 'prateleiras/cadastro.html', {
            'prateleira': prateleira,
            'estantes': estantes
        })
        
    except Exception as e:
        messages.error(request, f'Erro ao editar prateleira: {e}')
        return redirect('prateleiras:lista')


@login_required
def excluir_prateleira(request, prateleira_id):
    """Excluir prateleira (desativa)"""
    try:
        prateleira = PrateleiraRepository.get_by_id(prateleira_id)
        
        if not prateleira:
            messages.error(request, 'Prateleira não encontrada!')
            return redirect('prateleiras:lista')
        
        PrateleiraRepository.delete(prateleira_id)
        messages.success(request, f'Prateleira "{prateleira["descricao"]}" excluída com sucesso!')
        
    except Exception as e:
        messages.error(request, f'Erro ao excluir prateleira: {e}')
    
    return redirect('prateleiras:lista')
