from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from datetime import date, datetime
import re
from loja.apps.apps_administrador.cliente.models import Cliente, Endereco
from loja.apps.site_loja.forms.login import LoginForm

def login(request):
    form_login = LoginForm()
    context = {
        'form_login': form_login
    }
    if request.method == "GET":
        return render(request, "conta/login.html", context=context)

    elif request.method == "POST":
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                email = form.cleaned_data['email']
                senha = form.cleaned_data['password']

                user_cliente = authenticate(username=email, password=senha)
                if user_cliente:
                    cliente = Cliente.objects.get(user_cliente_id=user_cliente.id)
                    if cliente.is_active:
                        login_django(request, user_cliente)
                        return redirect('/')
                    else:
                        messages.error(request, "Usuário inativo!")
                        return render(request, "conta/login.html", context=context)
                else:
                    messages.error(request, "E-mail ou senha incorretos!")
                    return render(request, "conta/login.html", context=context)
        except Exception as e:
            messages.error(request, "E-mail ou senha incorretos!")
            return render(request, "conta/login.html", context=context)

@login_required
def sair(request):
    logout(request)
    return render(request, "conta/logout.html")

def create_count(request):
    form_login = LoginForm()
    context = {
        'form_login': form_login
    }
    if request.method == "GET":
        return render(request, "conta/create_conta.html")
    elif request.method == "POST":
        nome = request.POST.get('nome-create-conta')
        email = request.POST.get('email-create-conta')
        senha = request.POST.get('senha-create-conta')

        telefone = request.POST.get('telefone-create-conta')
        cpf_cnpj = request.POST.get('cpfcnpj-create-conta')
        data_nascimento = request.POST.get('data-create-conta')

        cep = request.POST.get('cep')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        rua = request.POST.get('logradouro')
        nr_casa = request.POST.get('nr-casa')

        try:

            user_verifica = User.objects.filter(email__iexact=email).exists()
            if user_verifica:
                messages.error(request, "Este e-mail já existe por favor digite um e-mail diferente!")
                return redirect('/criar-conta/')

            user_cliente = User (
                first_name = nome, 
                last_name = "",
                username = email,
                email = email,
                password = make_password(senha),
                is_active = False,
                is_staff = False,
                is_superuser = False,
            )
            user_cliente.save()

            cpf_valida = re.compile("^(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}|\d{3}\.?\d{3}\.?\d{3}-?\d{2})$")
            busca = cpf_valida.search(cpf_cnpj)
            if busca is None:
                messages.error(request, "Este CPF ou CNPJ não é valido!")
                return redirect('/criar-conta/')
                
            r = re.compile(r'[^0-9]')
            cpf_cnpj = r.sub('', cpf_cnpj)
            telefone = r.sub('', telefone)

            cpf_verifica = Cliente.objects.filter(cpf_cnpj__iexact=cpf_cnpj).exists()
            if cpf_verifica:
                messages.error(request, "Este CPF ou CNPJ já existe por favor digite um CPF ou CNPJ diferente!")
                return redirect('/criar-conta/')

            data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()

            cliente = Cliente (
                telefone = telefone,
                cpf_cnpj = cpf_cnpj,
                data_nascimento = data_nascimento,
                is_active = True,
                user_cliente = user_cliente
            )
            cliente.save()

            if(not(nr_casa and nr_casa.strip())): 
                nr_casa = None
            else: 
                nr_casa = int(nr_casa)
            
            cliente_endereco = Endereco (
                cep = cep,
                estado = estado,
                cidade = cidade,
                bairro = bairro,
                logradouro = rua,
                nr_casa = nr_casa,
                user_cliente = user_cliente
            )
            
            cliente_endereco.save()

            messages.success(request, "Conta criada com sucesso por favor faça login agora!")
            return render(request, "conta/login.html", context=context)

        except Exception as e:
            print(e)
            messages.error(request, "Conta não criada algum erro inesperado. Tente novamente!")
            return redirect('/criar-conta/')
        