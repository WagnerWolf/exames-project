from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from atendimentos.forms import AtendimentoForm
from .models import Atendimento
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
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
    
    if request.method != 'POST':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename = Relatório '+ str(date.today()) +' .pdf'
        response['Content-Transfer-Encoding'] = 'binary'

        atendimentos = Atendimento.objects.order_by('dataAtendimento')

        html_string = render_to_string('atendimentos/pdf-output.html',{'atendimentos':atendimentos})
        html = HTML(string=html_string)
        

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output=open(output.name, 'rb')
            response.write(output.read())

        return response
    else:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename = Relatório '+ str(date.today()) +' .pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        ano = request.POST.get('ano')
        mes = request.POST.get('mes')
        mesnome = {'01':'Janeiro','02':'Fevereiro','03':'Março','04':'Abril','05':'Maio','06': 'Junho','07':'Julho','08':'Agosto', '09':'Setembro', '10':'Outubro','11':'Novembro','12':'Dezembro'}
        atendimentos = Atendimento.objects.order_by('dataAtendimento').filter(dataAtendimento__year=ano, 
                      dataAtendimento__month=mes)

        html_string = render_to_string('atendimentos/pdf-output-filtrado.html',{'atendimentos':atendimentos,'mes':mesnome[mes],'ano':ano})
        html = HTML(string=html_string)
        

        result = html.write_pdf()

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output=open(output.name, 'rb')
            response.write(output.read())

        return response

@login_required
def carta_atendimento(request, atendimento_id):
    atendimento = Atendimento.objects.get(id = atendimento_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename = Relatório '+ str(date.today()) +' .pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    html_string = render_to_string('atendimentos/pdf-output-carta.html',{'atendimento':atendimento})
    html = HTML(string=html_string)
    

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output=open(output.name, 'rb')
        response.write(output.read())

    return response