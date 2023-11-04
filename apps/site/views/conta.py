from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from ...admin.cliente.models import Cliente, Endereco
from ..forms.create_conta import (
    CreateUserForm,
    CreateClienteForm,
    CreateClienteEnderecoForm,
)
from ..forms.login import LoginForm
from ..utils import is_cpf_valido, is_cnpj_valido


def login(request):
    form_login = LoginForm()
    context = {"form_login": form_login}
    if request.method == "GET":
        return render(request, "conta/login.html", context=context)

    elif request.method == "POST":
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                email = form.cleaned_data["email"]
                senha = form.cleaned_data["password"]

                user_cliente = authenticate(username=email, password=senha)
                if user_cliente:
                    if user_cliente.is_staff or user_cliente.is_superuser:
                        messages.error(
                            request, "você não é cliente e sim administrador"
                        )
                        return render(request, "conta/login.html", context=context)
                    else:
                        cliente = Cliente.objects.get(user_cliente_id=user_cliente.id)
                        if cliente.is_active:
                            login_django(request, user_cliente)
                            return redirect("/")
                        else:
                            messages.error(request, "Usuário inativo!")
                            return render(request, "conta/login.html", context=context)
                else:
                    messages.error(request, "E-mail ou senha incorretos!")
                    return render(request, "conta/login.html", context=context)
            else:
                messages.error(request, "Você não informou os dados obrigatórios!")
                return render(request, "conta/login.html", context=context)
        except Exception as e:
            messages.error(
                request, "Aconteceu algum erro insesperado favor tentar novamente!"
            )
            return render(request, "conta/login.html", context=context)


@login_required
def sair(request):
    logout(request)
    return render(request, "conta/logout.html")


def create_count(request):
    form_login = LoginForm()
    context = {"form_login": form_login}

    form_user = CreateUserForm()
    form_cliente = CreateClienteForm()
    form_cliente_endereco = CreateClienteEnderecoForm()
    context_create_conta = {
        "form_user": form_user,
        "form_cliente": form_cliente,
        "form_cliente_endereco": form_cliente_endereco,
    }
    if request.method == "GET":
        return render(request, "conta/create_conta.html", context=context_create_conta)
    elif request.method == "POST":
        create_form_user = CreateUserForm(request.POST)
        create_form_cliente = CreateClienteForm(request.POST)
        create_form_cliente_endereco = CreateClienteEnderecoForm(request.POST)

        if (
            create_form_user.is_valid()
            and create_form_cliente.is_valid()
            and create_form_cliente_endereco.is_valid()
        ):
            nome = create_form_user.cleaned_data["first_name"]
            email = create_form_user.cleaned_data["email"]
            senha = create_form_user.cleaned_data["password"]

            telefone = create_form_cliente.cleaned_data["telefone"]
            cpf_cnpj = create_form_cliente.cleaned_data["cpf_cnpj"]
            data_nascimento = create_form_cliente.cleaned_data["data_nascimento"]

            cep = create_form_cliente_endereco.cleaned_data["cep"]
            estado = create_form_cliente_endereco.cleaned_data["estado"]
            cidade = create_form_cliente_endereco.cleaned_data["cidade"]
            bairro = create_form_cliente_endereco.cleaned_data["bairro"]
            rua = create_form_cliente_endereco.cleaned_data["logradouro"]
            nr_casa = create_form_cliente_endereco.cleaned_data["nr_casa"]

            try:
                user_verifica = User.objects.filter(email__iexact=email).exists()
                if user_verifica:
                    messages.error(
                        request,
                        "Este e-mail já existe por favor digite um e-mail diferente!",
                    )
                    return redirect("/criar-conta/")

                cpf_valida = re.compile(
                    "^(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}|\d{3}\.?\d{3}\.?\d{3}-?\d{2})$"
                )
                busca = cpf_valida.search(cpf_cnpj)
                if busca is None:
                    messages.error(request, "Este formato de CPF ou CNPJ não é valido!")
                    return redirect("/criar-conta/")

                r = re.compile(r"[^0-9]")
                cpf_cnpj = r.sub("", cpf_cnpj)
                if len(cpf_cnpj) == 11:
                    valida_cpf = is_cpf_valido(cpf_cnpj)
                    if valida_cpf is False:
                        messages.error(request, "Este CPF não é valido!")
                        return redirect("/criar-conta/")
                if len(cpf_cnpj) == 14:
                    valida_cnpj = is_cnpj_valido(cpf_cnpj)
                    if valida_cnpj is False:
                        messages.error(request, "Este CNPJ não é valido!")
                        return redirect("/criar-conta/")

                cpf_verifica = Cliente.objects.filter(
                    cpf_cnpj__iexact=cpf_cnpj
                ).exists()
                if cpf_verifica:
                    messages.error(
                        request,
                        "Este CPF ou CNPJ já existe por favor digite um CPF ou CNPJ diferente!",
                    )
                    return redirect("/criar-conta/")
                telefone = r.sub("", telefone)

                user_cliente = User(
                    first_name=nome,
                    last_name="",
                    username=email,
                    email=email,
                    password=make_password(senha),
                    is_active=True,
                    is_staff=False,
                    is_superuser=False,
                )
                user_cliente.save()

                cliente = Cliente(
                    telefone=telefone,
                    cpf_cnpj=cpf_cnpj,
                    data_nascimento=data_nascimento,
                    is_active=True,
                    user_cliente=user_cliente,
                )
                cliente.save()

                if not (nr_casa and nr_casa.strip()):
                    nr_casa = None
                else:
                    nr_casa = int(nr_casa)

                cliente_endereco = Endereco(
                    cep=cep,
                    estado=estado,
                    cidade=cidade,
                    bairro=bairro,
                    logradouro=rua,
                    nr_casa=nr_casa,
                    user_cliente=user_cliente,
                )

                cliente_endereco.save()

                messages.success(
                    request, "Conta criada com sucesso por favor faça login agora!"
                )
                return render(request, "conta/login.html", context=context)

            except Exception as e:
                messages.error(
                    request, "Conta não criada algum erro inesperado. Tente novamente!"
                )
                return redirect("/criar-conta/")
        else:
            messages.error(
                request,
                "Algum campo obrigatorio não preenchido, favor tentar novamente!",
            )
            return redirect("/criar-conta/")
