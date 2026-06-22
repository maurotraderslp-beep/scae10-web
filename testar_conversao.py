import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

import django
django.setup()

from documentos.file_utils import converter_foto_path

# Testar com diferentes caminhos
caminhos = [
    'Fotos/foto teste aluno.png',
    'C:\\SCAE10\\Fotos\\01 - ABNER SILVA.jpg',
    'C:\\Users\\profm\\OneDrive\\Área de Trabalho\\foto teste aluno.png',
    '01 - ABNER SILVA.jpg',
]

print("=" * 80)
print("TESTANDO CONVERSÃO DE CAMINHOS")
print("=" * 80)

for caminho in caminhos:
    print(f"\nOriginal: {caminho}")
    resultado = converter_foto_path(caminho)
    print(f"Convertido: {resultado}")
    print("-" * 80)
