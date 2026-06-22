"""
URLs de Calendário Escolar
"""
from django.urls import path
from . import views

app_name = 'calendarios'

urlpatterns = [
    path('', views.calendario_view, name='calendario'),
    path('upload/', views.upload_calendario, name='upload'),
    path('visualizar/', views.visualizar_calendario, name='visualizar'),
    path('excluir/', views.excluir_calendario, name='excluir'),
]
