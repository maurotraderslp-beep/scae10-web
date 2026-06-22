import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')
django.setup()

from django.conf import settings
from documentos.aluno_repository import aluno_repository
from documentos.file_utils import converter_foto_path

# Testar aluno ID 1
aluno = aluno_repository.get_by_id(1)

print("=" * 80)
print("TESTE COMPLETO - ALUNO ID 1")
print("=" * 80)

print(f"\n1. DADOS DO ALUNO:")
print(f"   ID: {aluno['id']}")
print(f"   NOME: {aluno['nome']}")
print(f"   FOTO_PATH (banco): {aluno.get('foto_path', 'N/A')}")

print(f"\n2. CONFIGURAÇÕES DJANGO:")
print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   DEBUG: {settings.DEBUG}")

print(f"\n3. CONVERSÃO DA FOTO:")
foto_path = aluno.get('foto_path', '')
foto_url = converter_foto_path(foto_path)
print(f"   Path original: {foto_path}")
print(f"   URL convertida: {foto_url}")

if foto_url:
    # Verificar se arquivo existe
    import os
    arquivo_path = os.path.join(settings.MEDIA_ROOT, foto_url.replace('/media/', ''))
    print(f"   Path do arquivo: {arquivo_path}")
    print(f"   Arquivo existe: {os.path.exists(arquivo_path)}")
    
print(f"\n4. URL PARA ACESSAR:")
if foto_url:
    print(f"   No navegador: http://127.0.0.1:8000{foto_url}")
    print(f"   Ou: http://192.168.1.192:8000{foto_url}")

print("\n" + "=" * 80)
