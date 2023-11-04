from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from ..utils import GeraPix
from ...admin.produto.models import Produto
from ...admin.cliente.models import Endereco, Cliente
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
def adiciona_carrinho(request):
    if request.method == "POST":
        id_produto = request.POST.get("id_produto")
        qtd = request.POST.get("qtd")

        produto = Produto.objects.filter(id=id_produto).first()

        if int(qtd) > int(produto.quantidade):
            return JsonResponse(
                {"msg": "quantidade indisponivel!"},
                status=200,
                content_type="application/json",
            )

        if produto.desconto is not None and produto.desconto != "":
            valor = produto.valor - produto.desconto
        else:
            valor = produto.valor

        produto = {
            "id": produto.id,
            "nome": produto.nome,
            "imagem_principal": str(produto.imagem_principal),
            "valor": str(valor),
        }

        if produto:
            return JsonResponse(produto, status=200, content_type="application/json")
        else:
            return JsonResponse(False, status=400, content_type="application/json")


@login_required(login_url="/login")
def carrinho(request):
    if request.method == "GET":
        return render(request, "carrinho/index.html")


@login_required(login_url="/login")
def dados_perfil_carrinho(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            cliente = Cliente.objects.filter(user_cliente_id=user.id).first()
            if cliente:
                if len(cliente.cpf_cnpj) == 11:
                    cpf_cnpj = f"{cliente.cpf_cnpj[0:3]}.{cliente.cpf_cnpj[3:6]}.{cliente.cpf_cnpj[6:9]}-{cliente.cpf_cnpj[9:11]}"
                elif len(cliente.cpf_cnpj) == 14:
                    "55.555.555/5555-55"
                    cpf_cnpj = f"{cliente.cpf_cnpj[0:2]}.{cliente.cpf_cnpj[2:5]}.{cliente.cpf_cnpj[5:8]}/{cliente.cpf_cnpj[8:12]}-{cliente.cpf_cnpj[12:14]}"

                telefone = f"({cliente.telefone[0:2]}) {cliente.telefone[2:7]}-{cliente.telefone[7:11]}"
                data_nascimento = cliente.data_nascimento
                avatar = cliente.avatar
            else:
                cpf_cnpj = ""
                telefone = ""
                data_nascimento = ""
                avatar = " "

            endereco = Endereco.objects.filter(user_cliente_id=user.id).first()
            if endereco:
                cep = endereco.cep
                estado = endereco.estado
                cidade = endereco.cidade
                logradouro = endereco.logradouro
                nr_casa = endereco.nr_casa
            else:
                cep = ""
                estado = ""
                cidade = ""
                logradouro = ""
                nr_casa = ""

            perfil = {
                "nome": user.first_name,
                "email": user.email,
                "telefone": telefone,
                "cpf_cnpj": cpf_cnpj,
                "data_nascimento": data_nascimento,
                "avatar": avatar,
                "cep": cep,
                "estado": estado,
                "cidade": cidade,
                "logradouro": logradouro,
                "nr_casa": nr_casa,
            }
            return render(request, "carrinho/dados_perfil.html", {"perfil": perfil})


@login_required(login_url="/login")
def frete_carrinho(request):
    return render(request, "carrinho/frete_carrinho.html")


@login_required(login_url="/login")
def forma_pagamento_carrinho(request):
    return render(request, "carrinho/forma_pagamento_carrinho.html")


@method_decorator(csrf_exempt, name="dispatch")
@login_required(login_url="/login")
def pagamento_carrinho(request):
    if request.method == "GET":
        return render(request, "carrinho/pagamento_carrinho.html")
    elif request.method == "POST":
        lista_produtos = json.loads(request.POST.get("produtos"))
        produtos = []
        for i in lista_produtos:
            id = int(i["id"])
            produto = Produto.objects.filter(id=id).first()

            if int(i["qtd"]) > produto.quantidade:
                return JsonResponse(
                    {"msg": "quantidade indisponivel!"},
                    status=200,
                    content_type="application/json",
                )

            produto = {
                "nome": produto.nome,
                "quantidade": i["qtd"],
                "imagem_principal": str(produto.imagem_principal),
                "valor": produto.valor,
            }
            produtos.append(produto)

        return JsonResponse(
            {"produtos": produtos}, status=200, content_type="application/json"
        )


@method_decorator(csrf_exempt, name="dispatch")
@login_required(login_url="/login")
def gerar_pagamento(request):
    if request.method == "POST":
        lista_produtos = json.loads(request.POST.get("produtos"))
        valor = 0.00
        for i in lista_produtos:
            id = int(i["id"])
            produto = Produto.objects.filter(id=id).first()

            quantidade = int(i["qtd"])
            if quantidade > produto.quantidade:
                return JsonResponse(
                    {"msg": "quantidade indisponivel!"},
                    status=200,
                    content_type="application/json",
                )

            valor = valor + (float(produto.valor) * quantidade)

        gera_pix = GeraPix()
        url = gera_pix.envia_dados(valor=268)

        return JsonResponse({"img": url}, status=200, content_type="application/json")
