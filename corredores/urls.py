from django.urls import path
from . import views

app_name = 'corredores'

urlpatterns = [
    path('', views.lista_corredores, name='lista'),
    path('cadastro/', views.cadastro_corredor, name='cadastro'),
    path('<int:corredor_id>/editar/', views.editar_corredor, name='editar'),
    path('<int:corredor_id>/excluir/', views.excluir_corredor, name='excluir'),
]
