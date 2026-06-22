from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from documentos.corredor_repository import CorredorRepository


@login_required
def lista_corredores(request):
    """Listar todos os corredores"""
    try:
        corredores = CorredorRepository.get_all()
    except Exception as e:
        messages.error(request, f'Erro ao carregar corredores: {e}')
        corredores = []
    
    return render(request, 'corredores/lista.html', {
        'corredores': corredores
    })


@login_required
def cadastro_corredor(request):
    """Cadastrar novo corredor"""
    if request.method == 'POST':
        try:
            # Processar upload de imagem
            foto_path = ''
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                import os
                from django.conf import settings
                
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'corredores')
                os.makedirs(fotos_dir, exist_ok=True)
                
                # Salvar foto
                import unicodedata
                nome_arquivo = foto.name
                nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
                nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode('ASCII')
                nome_arquivo = nome_arquivo.replace(' ', '_')
                
                caminho_completo = os.path.join(fotos_dir, nome_arquivo)
                
                with open(caminho_completo, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                foto_path = f'corredores/{nome_arquivo}'
            
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'foto_path': foto_path,
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Código é obrigatório!')
                return render(request, 'corredores/cadastro.html', {'corredor': dados})
            
            if not dados['descricao']:
                messages.error(request, 'Descrição é obrigatória!')
                return render(request, 'corredores/cadastro.html', {'corredor': dados})
            
            CorredorRepository.create(dados)
            messages.success(request, f'Corredor "{dados["descricao"]}" cadastrado com sucesso!')
            return redirect('corredores:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar corredor: {e}')
    
    return render(request, 'corredores/cadastro.html', {'corredor': {}})


@login_required
def editar_corredor(request, corredor_id):
    """Editar corredor existente"""
    try:
        corredor = CorredorRepository.get_by_id(corredor_id)
        
        if not corredor:
            messages.error(request, 'Corredor não encontrado!')
            return redirect('corredores:lista')
        
        if request.method == 'POST':
            # Processar upload de imagem
            foto_path = corredor.get('foto_path', '')
            if request.FILES.get('foto'):
                foto = request.FILES['foto']
                import os
                from django.conf import settings
                
                fotos_dir = os.path.join(settings.MEDIA_ROOT, 'corredores')
                os.makedirs(fotos_dir, exist_ok=True)
                
                # Salvar foto
                import unicodedata
                nome_arquivo = foto.name
                nome_arquivo = unicodedata.normalize('NFKD', nome_arquivo)
                nome_arquivo = nome_arquivo.encode('ASCII', 'ignore').decode('ASCII')
                nome_arquivo = nome_arquivo.replace(' ', '_')
                
                caminho_completo = os.path.join(fotos_dir, nome_arquivo)
                
                with open(caminho_completo, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                foto_path = f'corredores/{nome_arquivo}'
            
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'foto_path': foto_path,
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Código é obrigatório!')
                return render(request, 'corredores/cadastro.html', {'corredor': {**corredor, **dados}})
            
            if not dados['descricao']:
                messages.error(request, 'Descrição é obrigatória!')
                return render(request, 'corredores/cadastro.html', {'corredor': {**corredor, **dados}})
            
            CorredorRepository.update(corredor_id, dados)
            messages.success(request, f'Corredor "{dados["descricao"]}" atualizado com sucesso!')
            return redirect('corredores:lista')
        
        return render(request, 'corredores/cadastro.html', {'corredor': corredor})
        
    except Exception as e:
        messages.error(request, f'Erro ao editar corredor: {e}')
        return redirect('corredores:lista')


@login_required
def excluir_corredor(request, corredor_id):
    """Excluir corredor (desativa)"""
    try:
        corredor = CorredorRepository.get_by_id(corredor_id)
        
        if not corredor:
            messages.error(request, 'Corredor não encontrado!')
            return redirect('corredores:lista')
        
        CorredorRepository.delete(corredor_id)
        messages.success(request, f'Corredor "{corredor["descricao"]}" excluído com sucesso!')
        
    except Exception as e:
        messages.error(request, f'Erro ao excluir corredor: {e}')
    
    return redirect('corredores:lista')
