from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls')),
    path('alunos/', include('alunos.urls')),
    path('corredores/', include('corredores.urls')),
    path('estantes/', include('estantes.urls')),
    path('prateleiras/', include('prateleiras.urls')),
    path('equipamentos/', include('equipamentos.urls')),
    path('calendarios/', include('calendarios.urls')),
    path('solicitacoes/', include('solicitacoes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
