"""
Views de Calendário Escolar
Upload e visualização de PDF do calendário
"""
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse, Http404


@login_required
def calendario_view(request):
    """Exibir calendário escolar com upload e visualização"""
    
    # Verificar se já existe um PDF de calendário
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'calendario', 'calendario_escolar.pdf')
    pdf_exists = os.path.exists(pdf_path)
    
    context = {
        'pdf_exists': pdf_exists,
        'pdf_url': '/media/calendario/calendario_escolar.pdf' if pdf_exists else None
    }
    
    return render(request, 'calendarios/calendario.html', context)


@login_required
def upload_calendario(request):
    """Fazer upload do PDF do calendário escolar"""
    if request.method == 'POST' and request.FILES.get('calendario_pdf'):
        try:
            pdf_file = request.FILES['calendario_pdf']
            
            # Validar se é PDF
            if not pdf_file.content_type == 'application/pdf':
                messages.error(request, 'O arquivo deve ser um PDF!')
                return redirect('calendarios:calendario')
            
            # Criar pasta se não existir
            calendario_dir = os.path.join(settings.MEDIA_ROOT, 'calendario')
            os.makedirs(calendario_dir, exist_ok=True)
            
            # Salvar arquivo (sempre com o mesmo nome para substituir)
            pdf_path = os.path.join(calendario_dir, 'calendario_escolar.pdf')
            
            with open(pdf_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)
            
            messages.success(request, 'Calendário escolar enviado com sucesso!')
            return redirect('calendarios:calendario')
            
        except Exception as e:
            messages.error(request, f'Erro ao enviar calendário: {str(e)}')
            return redirect('calendarios:calendario')
    
    return redirect('calendarios:calendario')


@login_required
def visualizar_calendario(request):
    """Visualizar o PDF do calendário escolar"""
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'calendario', 'calendario_escolar.pdf')
    
    print(f"[DEBUG] Tentando abrir PDF: {pdf_path}")
    print(f"[DEBUG] PDF existe: {os.path.exists(pdf_path)}")
    
    if not os.path.exists(pdf_path):
        print(f"[ERRO] PDF não encontrado em: {pdf_path}")
        raise Http404("Calendário não encontrado")
    
    try:
        response = FileResponse(
            open(pdf_path, 'rb'),
            content_type='application/pdf'
        )
        
        # Importante: definir headers para visualização inline
        response['Content-Disposition'] = 'inline; filename="calendario_escolar.pdf"'
        response['Content-Length'] = os.path.getsize(pdf_path)
        
        print(f"[SUCESSO] PDF servido: {os.path.getsize(pdf_path)} bytes")
        return response
    except Exception as e:
        print(f"[ERRO] Ao servir PDF: {e}")
        raise Http404(f"Erro ao abrir PDF: {str(e)}")


@login_required
def excluir_calendario(request):
    """Excluir o PDF do calendário escolar"""
    if request.method == 'POST':
        try:
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'calendario', 'calendario_escolar.pdf')
            
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                messages.success(request, 'Calendário excluído com sucesso!')
            else:
                messages.error(request, 'Calendário não encontrado!')
                
        except Exception as e:
            messages.error(request, f'Erro ao excluir calendário: {str(e)}')
    
    return redirect('calendarios:calendario')
