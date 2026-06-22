"""
Views de Equipamentos
CRUD para EQUIPAMENTO_DATA_SHOW
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from documentos.equipamento_repository import EquipamentoRepository


@login_required
def lista_equipamentos(request):
    """Listar todos os equipamentos"""
    equipamentos = EquipamentoRepository.get_all()
    return render(request, 'equipamentos/lista.html', {
        'equipamentos': equipamentos
    })


@login_required
def cadastro_equipamento(request):
    """Cadastrar novo equipamento"""
    if request.method == 'POST':
        try:
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'localizacao': request.POST.get('localizacao', '').strip().upper(),
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Informe o código do equipamento!')
                return render(request, 'equipamentos/cadastro.html', {'equipamento': dados})
            
            if not dados['descricao']:
                messages.error(request, 'Informe a descrição do equipamento!')
                return render(request, 'equipamentos/cadastro.html', {'equipamento': dados})
            
            # Criar equipamento
            EquipamentoRepository.create(dados)
            messages.success(request, f'Equipamento {dados["codigo"]} cadastrado com sucesso!')
            return redirect('equipamentos:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar equipamento: {str(e)}')
            return render(request, 'equipamentos/cadastro.html', {
                'equipamento': {
                    'codigo': request.POST.get('codigo', ''),
                    'descricao': request.POST.get('descricao', ''),
                    'localizacao': request.POST.get('localizacao', ''),
                    'ativo': request.POST.get('ativo', 'S')
                }
            })
    
    return render(request, 'equipamentos/cadastro.html', {'equipamento': {}})


@login_required
def editar_equipamento(request, equipamento_id):
    """Editar equipamento"""
    equipamento = EquipamentoRepository.get_by_id(equipamento_id)
    
    if not equipamento:
        messages.error(request, 'Equipamento não encontrado!')
        return redirect('equipamentos:lista')
    
    if request.method == 'POST':
        try:
            dados = {
                'codigo': request.POST.get('codigo', '').strip().upper(),
                'descricao': request.POST.get('descricao', '').strip().upper(),
                'localizacao': request.POST.get('localizacao', '').strip().upper(),
                'ativo': request.POST.get('ativo', 'S')
            }
            
            # Validações
            if not dados['codigo']:
                messages.error(request, 'Informe o código do equipamento!')
                return render(request, 'equipamentos/cadastro.html', {
                    'equipamento': dados,
                    'editando': True
                })
            
            if not dados['descricao']:
                messages.error(request, 'Informe a descrição do equipamento!')
                return render(request, 'equipamentos/cadastro.html', {
                    'equipamento': dados,
                    'editando': True
                })
            
            # Atualizar equipamento
            EquipamentoRepository.update(equipamento_id, dados)
            messages.success(request, f'Equipamento {dados["codigo"]} atualizado com sucesso!')
            return redirect('equipamentos:lista')
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar equipamento: {str(e)}')
    
    # GET - carregar dados do equipamento
    return render(request, 'equipamentos/cadastro.html', {
        'equipamento': {
            'id': equipamento.get('id'),
            'codigo': equipamento.get('codigo'),
            'descricao': equipamento.get('descricao'),
            'localizacao': equipamento.get('localizacao'),
            'ativo': equipamento.get('ativo')
        },
        'editando': True
    })


@login_required
def excluir_equipamento(request, equipamento_id):
    """Excluir equipamento (desativação lógica)"""
    try:
        equipamento = EquipamentoRepository.get_by_id(equipamento_id)
        if equipamento:
            EquipamentoRepository.delete(equipamento_id)
            messages.success(request, f'Equipamento {equipamento.get("codigo")} desativado com sucesso!')
        else:
            messages.error(request, 'Equipamento não encontrado!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir equipamento: {str(e)}')
    
    return redirect('equipamentos:lista')
