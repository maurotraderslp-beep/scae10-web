"""
URLs de Alunos
"""
from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.lista_alunos, name='lista'),
    path('<int:aluno_id>/', views.detalhe_aluno, name='detalhe'),
    path('cadastro/', views.cadastro_aluno, name='cadastro'),
    path('<int:aluno_id>/editar/', views.editar_aluno, name='editar'),
    path('<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir'),
    path('api/resolucoes/', views.buscar_resolucoes_por_modalidade, name='buscar_resolucoes'),
    path('testar-foto/', views.testar_foto, name='testar_foto'),
    path('teste-upload/', views.teste_upload, name='teste_upload'),
]
