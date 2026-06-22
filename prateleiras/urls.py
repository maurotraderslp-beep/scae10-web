from django.urls import path
from . import views

app_name = 'prateleiras'

urlpatterns = [
    path('', views.lista_prateleiras, name='lista'),
    path('cadastro/', views.cadastro_prateleira, name='cadastro'),
    path('<int:prateleira_id>/editar/', views.editar_prateleira, name='editar'),
    path('<int:prateleira_id>/excluir/', views.excluir_prateleira, name='excluir'),
]
