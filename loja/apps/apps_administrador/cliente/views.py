#Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#Mensagens Template
from django.contrib import messages
#Atenticação de Login e Session
from django.contrib.auth.decorators import login_required, permission_required
#User e filtros
from django.contrib.auth.models import User
from django.db.models import Q
#Retornar templates
from django.shortcuts import redirect, render
from .models import Cliente

@login_required(login_url="/admin")
@permission_required('cliente.view_cliente')
def cliente(request):
    users_clientes = User.objects.exclude(
        Q(is_superuser__gte=True),
        Q(is_staff__gte=True),
        Q(is_active__gte=True)
    ).all().order_by('-id')

    list_clientes = []
    for user_cliente in users_clientes:
        cliente = Cliente.objects.get(user_cliente_id=user_cliente.id)
        create_cliente = {
            'id': user_cliente.id,
            'nome': user_cliente.first_name + user_cliente.last_name,
            'email': user_cliente.email,
            'cpf_cnpj': cliente.cpf_cnpj,
            'telefone': cliente.telefone,
        }
        list_clientes.append(create_cliente)

    paginator = Paginator(list_clientes, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        clientes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        clientes = paginator.page(paginator.num_pages)
    return render(request, "clientes/index.html", {'clientes': clientes, 'len_clientes': len(list_clientes)})

@login_required(login_url="/admin")
@permission_required('cliente.view_cliente')
def search_cliente(request):
    list_clientes = Cliente.objects.all().order_by('-id')
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