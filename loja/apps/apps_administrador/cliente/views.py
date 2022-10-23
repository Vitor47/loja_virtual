#Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#Mensagens Template
from django.contrib import messages
#Atenticação de Login e Session
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required
#Retornar templates
from django.shortcuts import redirect, render

from .models import Cliente

@login_required(login_url="/admin")
def cliente(request):
    list_clientes = Cliente.objects.all()
    paginator = Paginator(list_clientes, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        clientes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        clientes = paginator.page(paginator.num_pages)
    return render(request, "clientes/index.html", {'clientes': clientes})

@login_required(login_url="/admin")
def search_cliente(request):
    list_clientes = Cliente.objects.all()
    consulta_nome = request.GET.get('pesquisar_por_nome')
    if consulta_nome is not None:
        list_clientes = list_clientes.filter(nome__icontains=consulta_nome)
    paginator = Paginator(list_clientes, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    try:
        clientes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        clientes = paginator.page(paginator.num_pages)
    return render(request, "produto/index.html", {'clientes': clientes})