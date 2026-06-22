"""
Utilitários para manipulação de caminhos de arquivos
"""
import os
from django.conf import settings


def converter_foto_path(foto_path):
    """
    Converte caminho da foto em URL web
    
    Exemplos:
        Fotos/01 - ABNER SILVA.jpg
        -> /media/Fotos/01 - ABNER SILVA.jpg
        
        C:\\SCAE10\\Fotos\\01 - ABNER SILVA.jpg (legado)
        -> /media/Fotos/01 - ABNER SILVA.jpg
        
        C:\\Users\\profm\\OneDrive\\foto.png (caminho qualquer)
        -> /media/Fotos/foto.png
    
    Retorna None se path é vazio
    """
    if not foto_path or foto_path.strip() == '':
        return None
    
    from django.conf import settings
    import os
    
    # Converter o caminho para URL web
    try:
        # Se o path começar com C:\SCAE10 (formato antigo), remover essa parte
        if foto_path.upper().startswith('C:\\SCAE10'):
            path_relativo = foto_path[10:]  # Remove 'C:\SCAE10'
            # Converter barras invertidas para normais
            path_relativo = path_relativo.replace('\\', '/')
        elif foto_path.upper().startswith('FOTOS/'):
            # Formato novo: Fotos/nome_arquivo.jpg
            path_relativo = foto_path
        else:
            # Para qualquer outro caminho Windows, extrair apenas o nome do arquivo
            nome_arquivo = os.path.basename(foto_path)
            path_relativo = f'Fotos/{nome_arquivo}'
            print(f"[DEBUG] Convertendo caminho: '{foto_path}' -> '{path_relativo}'")
        
        # Construir URL
        url_foto = f'/media/{path_relativo}'
        print(f"[DEBUG] URL da foto: {url_foto}")
        
        return url_foto
    except Exception as e:
        print(f"[ERRO] Ao converter foto: {e}")
        return None
