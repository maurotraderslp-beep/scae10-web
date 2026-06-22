from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from documentos.estante_repository import EstanteRepository
from documentos.corredor_repository import CorredorRepository


@login_required
def lista_estantes(request):
    """Listar todas as estantes"""
    try:
        estantes = EstanteRepository.get_all()
    except Exception as e:
        messages.error(request, f'Erro ao carregar estantes: {e}')
        estantes = []
    
    return render(request, 'estantes/lista.html', {
        'estantes': estantes
    })


@login_required
def cadastro_estante(request):
    """Cadastrar nova estante"""
    if request.method == 'POST':
        try:
            # Processar upload de imagem
            foto_path = ''
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                import os
                from django.conf import settings
                
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'estantes')
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
                
                foto_path = f'estantes/{nome_arquivo}'
            
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'corredor_id': int(request.POST.get('corredor_id')) if request.POST.get('corredor_id') else None,
                'foto_path': foto_path,
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Código é obrigatório!')
                corredores = CorredorRepository.get_all()
                return render(request, 'estantes/cadastro.html', {'estante': dados, 'corredores': corredores})
            
            if not dados['descricao']:
                messages.error(request, 'Descrição é obrigatória!')
                corredores = CorredorRepository.get_all()
                return render(request, 'estantes/cadastro.html', {'estante': dados, 'corredores': corredores})
            
            if not dados['corredor_id']:
                messages.error(request, 'Selecione um corredor!')
                corredores = CorredorRepository.get_all()
                return render(request, 'estantes/cadastro.html', {'estante': dados, 'corredores': corredores})
            
            EstanteRepository.create(dados)
            messages.success(request, f'Estante "{dados["descricao"]}" cadastrada com sucesso!')
            return redirect('estantes:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar estante: {e}')
    
    # GET - carregar corredores para o select
    try:
        corredores = CorredorRepository.get_all()
    except:
        corredores = []
    
    return render(request, 'estantes/cadastro.html', {
        'estante': {},
        'corredores': corredores
    })


@login_required
def editar_estante(request, estante_id):
    """Editar estante existente"""
    try:
        estante = EstanteRepository.get_by_id(estante_id)
        
        if not estante:
            messages.error(request, 'Estante não encontrada!')
            return redirect('estantes:lista')
        
        if request.method == 'POST':
            foto_path = estante.get('foto_path', '')
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                import os
                from django.conf import settings
                
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'estantes')
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
                
                foto_path = f'estantes/{nome_arquivo}'
            
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'corredor_id': int(request.POST.get('corredor_id')) if request.POST.get('corredor_id') else None,
                'foto_path': foto_path,
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Código é obrigatório!')
                corredores = CorredorRepository.get_all()
                return render(request, 'estantes/cadastro.html', {'estante': {**estante, **dados}, 'corredores': corredores})
            
            if not dados['descricao']:
                messages.error(request, 'Descrição é obrigatória!')
                corredores = CorredorRepository.get_all()
                return render(request, 'estantes/cadastro.html', {'estante': {**estante, **dados}, 'corredores': corredores})
            
            if not dados['corredor_id']:
                messages.error(request, 'Selecione um corredor!')
                corredores = CorredorRepository.get_all()
                return render(request, 'estantes/cadastro.html', {'estante': {**estante, **dados}, 'corredores': corredores})
            
            EstanteRepository.update(estante_id, dados)
            messages.success(request, f'Estante "{dados["descricao"]}" atualizada com sucesso!')
            return redirect('estantes:lista')
        
        # GET - carregar corredores para o select
        try:
            corredores = CorredorRepository.get_all()
        except:
            corredores = []
        
        return render(request, 'estantes/cadastro.html', {
            'estante': estante,
            'corredores': corredores
        })
        
    except Exception as e:
        messages.error(request, f'Erro ao editar estante: {e}')
        return redirect('estantes:lista')


@login_required
def excluir_estante(request, estante_id):
    """Excluir estante (desativa)"""
    try:
        estante = EstanteRepository.get_by_id(estante_id)
        
        if not estante:
            messages.error(request, 'Estante não encontrada!')
            return redirect('estantes:lista')
        
        EstanteRepository.delete(estante_id)
        messages.success(request, f'Estante "{estante["descricao"]}" excluída com sucesso!')
        
    except Exception as e:
        messages.error(request, f'Erro ao excluir estante: {e}')
    
    return redirect('estantes:lista')
