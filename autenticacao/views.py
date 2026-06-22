"""
Views de Autenticação
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.contrib.auth.models import User


def login_view(request):
    """
    Tela de login do sistema
    Usa autenticação padrão do Django
    """
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Informe usuário e senha.')
            return render(request, 'autenticacao/login.html')
        
        # Autentica usando sistema padrão do Django
        usuario = authenticate(
            request,
            username=username,
            password=password
        )
        
        if usuario is not None:
            # Login bem-sucedido
            django_login(request, usuario)
            
            messages.success(request, f'Bem-vindo, {usuario.first_name or usuario.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'autenticacao/login.html')


def logout_view(request):
    """Logout do sistema"""
    django_logout(request)
    return redirect('login')


def dashboard_view(request):
    """Dashboard principal do sistema"""
    context = {
        'total_alunos': 0,
        'total_professores': 0,
    }
    
    # Contar alunos do Firebird
    try:
        from documentos.aluno_repository import aluno_repository
        context['total_alunos'] = aluno_repository.get_ativos_count()
    except:
        pass  # Se der erro, mostra 0
    
    return render(request, 'autenticacao/dashboard.html', context)
