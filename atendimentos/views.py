from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, FileResponse
from django.urls import reverse
from atendimentos.forms import AtendimentoForm
from .models import Atendimento, Exame
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from datetime import date
# Create your views here.

def index(request):
    return render(request, 'atendimentos/index.html')

@login_required
def atendimentos(request):
    if request.method != 'POST':
        atendimentos = Atendimento.objects.order_by('dataAtendimento')
        paginator = Paginator(atendimentos, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {'atendimentos': atendimentos, 'page_obj':page_obj}
        return render(request, 'atendimentos/atendimentos.html', context)
    else:
        filtrado = True
        ano = request.POST.get('ano')
        mes = request.POST.get('mes')
        mesnome = {'01':'Janeiro','02':'Fevereiro','03':'Março','04':'Abril','05':'Maio','06': 'Junho','07':'Julho','08':'Agosto', '09':'Setembro', '10':'Outubro','11':'Novembro','12':'Dezembro'}
        atendimentos = Atendimento.objects.order_by('dataAtendimento').filter(dataAtendimento__year=ano, 
                      dataAtendimento__month=mes)
        paginator = Paginator(atendimentos, 15)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {'atendimentos': atendimentos, 'filtrado':filtrado,'ano':ano,'mes':mes,'mesnome':mesnome.get(mes),'page_obj':page_obj}
        return render(request, 'atendimentos/atendimentos.html', context)

@login_required
def atendimento(request, atendimento_id):
    atendimento = Atendimento.objects.get(id = atendimento_id)
    exames = list(atendimento.exames.all())
    context = {'atendimento': atendimento, 'exames': exames}
    return render (request, 'atendimentos/atendimento.html', context)

@login_required
def new_atendimento(request):
    if request.method != 'POST':
        """Se não é POST, cria um form em branco"""
        form = AtendimentoForm()
    else:
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit = False)
            atendimento.usuario = request.user
            atendimento = form.save()
            return HttpResponseRedirect(reverse('atendimentos'))
    context = {'form':form}
    return render(request, 'atendimentos/new_atendimento.html',context)


@login_required
def edit_atendimento(request, atendimento_id):
    atendimento = Atendimento.objects.get(id = atendimento_id)
    if request.method != 'POST':
        """Se não é POST, ele aparece o formulário já com os dados preenchidos para edição"""
        form = AtendimentoForm(instance=atendimento)
    else:
        """Se for POST, ele salva os dados"""
        form = AtendimentoForm(instance=atendimento, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('atendimento', args=[atendimento.id]))
    context = {'atendimento':atendimento, 'form':form}
    return render (request, 'atendimentos/edit_atendimento.html', context)

@login_required
def delete_atendimento(request, atendimento_id):
    if request.user.id != 1:
        raise Http404
    else:
        atendimento = Atendimento.objects.get(id = atendimento_id)
        atendimento.delete()
        return HttpResponseRedirect(reverse('atendimentos'))
    
    
@login_required
def report(request):
    atendimentos = Atendimento.objects.order_by('dataAtendimento')
    buffer = io.BytesIO()
    width,height=A4
    p = canvas.Canvas(buffer, pagesize=landscape(A4), bottomup=0)

    textob = p.beginText()
    textob.setTextOrigin(cm,cm)
    textob.setFont("Helvetica",10)

    lines = []
    for atendimento in atendimentos:
        # lines.append(str('Código: '+ atendimento.codigo+ ' Nome do Paciente: '+ atendimento.nomePaciente+ ' Exames: Falta colocar '+str(atendimento)+' Data: '+str(atendimento.dataAtendimento)))
        lines.append('Código: '+ atendimento.codigo)
        lines.append('Nome do Paciente: '+ atendimento.nomePaciente)
        for exame in atendimento.exames.all():
            lines.append('Exame: '+str(exame))
        lines.append('Data: '+str(atendimento.dataAtendimento))
        lines.append(' ')


    
    
    while len(lines) > 30 and len(lines) != 0:
        textob = p.beginText()
        textob.setTextOrigin(cm,cm)
        textob.setFont("Helvetica",10)
        for line in lines:
            textob.textLine(line)
        if(len(lines) <30):
            for line in lines:
                lines.pop(line)
        else:
            for i in range(30):
                lines.pop(0)
        p.drawText(textob)
        p.showPage()
    print(len(lines))
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="Relatorio "+ str(date.today())+ ".pdf")