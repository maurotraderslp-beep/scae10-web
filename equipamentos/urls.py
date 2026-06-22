"""
URLs de Equipamentos
"""
from django.urls import path
from . import views

app_name = 'equipamentos'

urlpatterns = [
    path('', views.lista_equipamentos, name='lista'),
    path('novo/', views.cadastro_equipamento, name='cadastro'),
    path('editar/<int:equipamento_id>/', views.editar_equipamento, name='editar'),
    path('excluir/<int:equipamento_id>/', views.excluir_equipamento, name='excluir'),
]
