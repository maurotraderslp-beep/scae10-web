"""
Gerador de Documentos Word/PDF
Usa mailmerge para preencher templates com MERGEFIELDs
Converte para PDF usando Word COM (Windows) ou LibreOffice
"""
import os
import tempfile
from mailmerge import MailMerge
from datetime import datetime


class GeradorDocumentos:
    """
    Gera documentos a partir de templates Word com MERGEFIELDs
    Preserva 100% dos templates do sistema Delphi
    """
    
    def __init__(self, template_path: str):
        """
        Inicializa com caminho do template Word
        
        Args:
            template_path: Caminho para arquivo .docx template
        """
        self.template_path = template_path
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template não encontrado: {template_path}")
    
    def gerar_documento(
        self, 
        dados: dict, 
        output_path: str,
        formato: str = 'pdf'
    ) -> bool:
        """
        Gera documento preenchido e salva em PDF ou Word
        
        Args:
            dados: Dicionário com dados para MERGEFIELDs
                   Ex: {'NOME_ALUNO': 'João', 'DATA_NASC': '01/01/2000'}
            output_path: Caminho para salvar arquivo final
            formato: 'pdf' ou 'docx'
        
        Returns:
            bool: True se gerou com sucesso
        """
        try:
            print(f"\n=== GERANDO DOCUMENTO ===")
            print(f"Template: {self.template_path}")
            print(f"Output: {output_path}")
            print(f"Formato: {formato}")
            
            # 1. Carrega template
            doc = MailMerge(self.template_path)
            
            # Lista mergefields encontrados
            fields = doc.get_merge_fields()
            print(f"\nMERGEFIELDs no template: {len(fields)}")
            print(f"Campos: {', '.join(sorted(list(fields))[:20])}")
            
            # 2. Preenche dados
            print(f"\nPreenchendo {len(dados)} campos:")
            for key, value in list(dados.items())[:10]:
                print(f"  {key} = {value}")
            if len(dados) > 10:
                print(f"  ... e mais {len(dados) - 10} campos")
            
            # Converte todos valores para string
            context = {k: str(v) if v is not None else '' for k, v in dados.items()}
            
            # Faz merge
            doc.merge(**context)
            print(f"\n✓ MERGEFIELDs preenchidos!")
            
            # 3. Salva documento
            if formato == 'pdf':
                # Salva Word temporário
                temp_word = tempfile.mktemp(suffix='.docx')
                doc.write(temp_word)
                print(f"✓ Word temporário: {temp_word}")
                
                # Converte para PDF
                sucesso = self._converter_para_pdf(temp_word, output_path)
                
                # Limpa arquivo temporário
                if os.path.exists(temp_word):
                    os.remove(temp_word)
                    print(f"✓ Arquivo temporário removido")
                
                return sucesso
            else:
                # Salva Word direto
                doc.write(output_path)
                print(f"✓ Documento Word salvo: {output_path}")
                return True
                
        except Exception as e:
            print(f"\n✗ ERRO ao gerar documento: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _converter_para_pdf(self, word_path: str, pdf_path: str) -> bool:
        """
        Converte Word para PDF
        
        Usa Word COM Automation no Windows (mesma lógica do Delphi)
        """
        try:
            print(f"\n=== CONVERTENDO WORD → PDF ===")
            print(f"Word: {word_path}")
            print(f"PDF: {pdf_path}")
            
            # Tenta usar Word COM (Windows com Word instalado)
            try:
                import win32com.client
                
                print("Usando Microsoft Word COM...")
                
                # Abre Word
                word = win32com.client.Dispatch('Word.Application')
                word.Visible = False  # Não mostra Word
                
                # Abre documento
                doc = word.Documents.Open(os.path.abspath(word_path))
                
                # Cria diretório se necessário
                output_dir = os.path.dirname(pdf_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                
                # Salva como PDF (17 = wdFormatPDF)
                doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
                doc.Close()
                
                # Fecha Word
                word.Quit()
                
                print(f"✓ PDF gerado com sucesso: {pdf_path}")
                return True
                
            except ImportError:
                print("Word COM não disponível (win32com não instalado)")
                raise Exception("Word COM não disponível")
            except Exception as e:
                print(f"Erro com Word COM: {e}")
                
                # Fallback: tenta LibreOffice
                print("\nTentando LibreOffice...")
                return self._converter_libreoffice(word_path, pdf_path)
                
        except Exception as e:
            print(f"✗ ERRO na conversão: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _converter_libreoffice(self, word_path: str, pdf_path: str) -> bool:
        """
        Converte Word para PDF usando LibreOffice
        Usado quando Word não está disponível
        """
        import subprocess
        
        try:
            print("Usando LibreOffice...")
            
            # Cria diretório se necessário
            output_dir = os.path.dirname(pdf_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Comando LibreOffice
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                word_path,
                '--outdir', output_dir
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # LibreOffice gera PDF com mesmo nome do Word
                temp_pdf = word_path.replace('.docx', '.pdf')
                
                if os.path.exists(temp_pdf):
                    # Renomeia para nome desejado
                    if temp_pdf != pdf_path:
                        os.rename(temp_pdf, pdf_path)
                    
                    print(f"✓ PDF gerado com LibreOffice: {pdf_path}")
                    return True
            
            print(f"✗ LibreOffice falhou: {result.stderr}")
            return False
            
        except FileNotFoundError:
            print("✗ LibreOffice não instalado")
            print("\nInstale LibreOffice:")
            print("  Windows: https://www.libreoffice.org/download/")
            print("  Linux: sudo apt install libreoffice")
            return False
        except Exception as e:
            print(f"✗ ERRO com LibreOffice: {e}")
            return False
