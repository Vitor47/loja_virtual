# Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Mensagens Template
from django.contrib import messages

# Atenticação de Login e Session
from django.contrib.auth.decorators import login_required, permission_required

# User e filtros
from django.contrib.auth.models import User
from django.db.models import Q

# Retornar templates
from django.shortcuts import redirect, render
from .models import Cliente, Endereco

# Permissões
from ..decorators import manager_required


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("cliente.view_cliente")
def cliente(request):
    if request.method == "GET":
        users_clientes = User.objects.filter(
            Q(is_superuser=False), Q(is_staff=False), Q(is_active=True)
        ).order_by("-id")

        list_clientes = []
        for user_cliente in users_clientes:
            cliente = Cliente.objects.filter(user_cliente__id=user_cliente.id).first()
            if cliente:
                if len(cliente.cpf_cnpj) == 11:
                    cpf_cnpj = f"{cliente.cpf_cnpj[0:3]}.{cliente.cpf_cnpj[3:6]}.{cliente.cpf_cnpj[6:9]}-{cliente.cpf_cnpj[9:11]}"
                elif len(cliente.cpf_cnpj) == 14:
                    "55.555.555/5555-55"
                    cpf_cnpj = f"{cliente.cpf_cnpj[0:2]}.{cliente.cpf_cnpj[2:5]}.{cliente.cpf_cnpj[5:8]}/{cliente.cpf_cnpj[8:12]}-{cliente.cpf_cnpj[12:14]}"
                telefone = f"({cliente.telefone[0:2]}) {cliente.telefone[2:7]}-{cliente.telefone[7:11]}"
                create_cliente = {
                    "id": user_cliente.id,
                    "nome": user_cliente.first_name,
                    "email": user_cliente.email,
                    "cpf_cnpj": cpf_cnpj,
                    "telefone": telefone,
                    "is_active": cliente.is_active,
                }
                list_clientes.append(create_cliente)

        paginator = Paginator(list_clientes, 10)
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            page = 1
        try:
            clientes = paginator.page(page)
        except (EmptyPage, InvalidPage):
            clientes = paginator.page(paginator.num_pages)
        return render(
            request,
            "clientes/index.html",
            {"clientes": clientes, "len_clientes": len(list_clientes)},
        )


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("cliente.view_cliente")
def search_cliente(request):
    if request.method == "GET":
        list_clientes = Cliente.objects.all().order_by("-id")
        consulta_nome = request.GET.get("pesquisar_por_nome")
        if consulta_nome is not None:
            users_clientes = User.objects.filter(
                Q(is_superuser=False),
                Q(is_staff=False),
                Q(is_active=True),
                Q(first_name__icontains=consulta_nome),
            ).order_by("-id")

            list_clientes = []
            for user_cliente in users_clientes:
                cliente = Cliente.objects.filter(
                    user_cliente__id=user_cliente.id
                ).first()
                if cliente:
                    if len(cliente.cpf_cnpj) == 11:
                        cpf_cnpj = f"{cliente.cpf_cnpj[0:3]}.{cliente.cpf_cnpj[3:6]}.{cliente.cpf_cnpj[6:9]}-{cliente.cpf_cnpj[9:11]}"
                    elif len(cliente.cpf_cnpj) == 14:
                        "55.555.555/5555-55"
                        cpf_cnpj = f"{cliente.cpf_cnpj[0:2]}.{cliente.cpf_cnpj[2:5]}.{cliente.cpf_cnpj[5:8]}/{cliente.cpf_cnpj[8:12]}-{cliente.cpf_cnpj[12:14]}"
                    telefone = f"({cliente.telefone[0:2]}) {cliente.telefone[2:7]}-{cliente.telefone[7:11]}"
                    create_cliente = {
                        "id": user_cliente.id,
                        "nome": user_cliente.first_name,
                        "email": user_cliente.email,
                        "cpf_cnpj": cpf_cnpj,
                        "telefone": telefone,
                        "is_active": cliente.is_active,
                    }
                    list_clientes.append(create_cliente)

        paginator = Paginator(list_clientes, 10)
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            page = 1
        try:
            clientes = paginator.page(page)
        except (EmptyPage, InvalidPage):
            clientes = paginator.page(paginator.num_pages)
        return render(
            request,
            "clientes/index.html",
            {"clientes": clientes, "len_clientes": len(list_clientes)},
        )


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("cliente.view_cliente")
def detalhes_cliente(request, id):
    if request.method == "GET":
        user_cliente = User.objects.filter(
            Q(is_superuser=False),
            Q(is_staff=False),
            Q(is_active=True),
        ).get(id=id)

        cliente = Cliente.objects.get(user_cliente_id=id)
        endereco = Endereco.objects.get(user_cliente_id=id)
        if cliente and endereco:
            if len(cliente.cpf_cnpj) == 11:
                cpf_cnpj = f"{cliente.cpf_cnpj[0:3]}.{cliente.cpf_cnpj[3:6]}.{cliente.cpf_cnpj[6:9]}-{cliente.cpf_cnpj[9:11]}"
            elif len(cliente.cpf_cnpj) == 14:
                "55.555.555/5555-55"
                cpf_cnpj = f"{cliente.cpf_cnpj[0:2]}.{cliente.cpf_cnpj[2:5]}.{cliente.cpf_cnpj[5:8]}/{cliente.cpf_cnpj[8:12]}-{cliente.cpf_cnpj[12:14]}"
            telefone = f"({cliente.telefone[0:2]}) {cliente.telefone[2:7]}-{cliente.telefone[7:11]}"

            dados_cliente = {
                "id": user_cliente.id,
                "nome": user_cliente.first_name,
                "email": user_cliente.email,
                "cpf_cnpj": cpf_cnpj,
                "telefone": telefone,
                "data_nascimento": cliente.data_nascimento,
                "cep": endereco.cep,
                "estado": endereco.estado,
                "cidade": endereco.cidade,
                "bairro": endereco.bairro,
                "logradouro": endereco.logradouro,
                "nr_casa": endereco.nr_casa,
            }

        return render(request, "clientes/detalhes.html", {"cliente": dados_cliente})


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("cliente.view_cliente")
def ativo_inativo(request, id):
    if request.method == "GET":
        cliente = Cliente.objects.get(user_cliente__id=id)
        if cliente:
            if cliente.is_active == True:
                cliente.is_active = False
                cliente.save()
            elif cliente.is_active == False:
                cliente.is_active = True
                cliente.save()

        messages.success(request, "Status atualizado do Cliente!")
        return redirect("/admin/cliente/")
