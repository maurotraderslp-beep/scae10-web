from django.urls import path
from . import views

app_name = 'estantes'

urlpatterns = [
    path('', views.lista_estantes, name='lista'),
    path('cadastro/', views.cadastro_estante, name='cadastro'),
    path('<int:estante_id>/editar/', views.editar_estante, name='editar'),
    path('<int:estante_id>/excluir/', views.excluir_estante, name='excluir'),
]
