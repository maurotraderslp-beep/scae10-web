"""
URLs de Solicitações
"""
from django.urls import path
from . import views

app_name = 'solicitacoes'

urlpatterns = [
    path('', views.lista_solicitacoes, name='lista'),
    path('nova/', views.cadastro_solicitacao, name='cadastro'),
    path('editar/<int:solicitacao_id>/', views.editar_solicitacao, name='editar'),
    path('excluir/<int:solicitacao_id>/', views.excluir_solicitacao, name='excluir'),
]
