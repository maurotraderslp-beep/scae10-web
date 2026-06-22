"""
Configurações de mídia para Django
"""
import os

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuração de arquivos de mídia
MEDIA_URL = '/media/'

# Pasta onde as fotos dos alunos estão armazenadas
# Exemplo: C:\SCAE10\Fotos
MEDIA_ROOT = r'C:\SCAE10'
