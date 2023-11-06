from django.shortcuts import render, redirect
import re
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from ..utils import is_cpf_valido, is_cnpj_valido
from ...admin.cliente.models import Cliente, Endereco


@login_required(login_url="/login")
def perfil_site(request):
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

                telefone = (
                    f"({cliente.telefone[0:2]})"
                    f" {cliente.telefone[2:7]}-{cliente.telefone[7:11]}"
                )
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
            return render(
                request, "perfil_site/index.html", {"perfil": perfil}
            )
        elif request.method == "POST":
            try:
                cliente = Cliente.objects.filter(
                    user_cliente_id=user.id
                ).first()
                if cliente:
                    image = request.POST.get("image")
                    if image:
                        for i in range(7):
                            if i == int(image):
                                cliente.avatar = f"ava{image}.webp"

                        cliente.save()
                        response = {
                            "message": True,
                        }
                        return JsonResponse(
                            response,
                            status=200,
                            content_type="application/json",
                        )
                    else:
                        nome = request.POST.get("nome")
                        email = request.POST.get("email")

                        telefone = request.POST.get("telefone")
                        cpf_cnpj = request.POST.get("cpf_cnpj")
                        data_nascimento = request.POST.get("data_nascimento")

                        cep = request.POST.get("cep")
                        estado = request.POST.get("estado")
                        cidade = request.POST.get("cidade")
                        bairro = request.POST.get("bairro")
                        logradouro = request.POST.get("logradouro")
                        nr_casa = request.POST.get("nr_casa")

                        try:
                            user_verifica = (
                                User.objects.exclude(id=user.id)
                                .filter(email__iexact=email)
                                .exists()
                            )
                            if user_verifica:
                                messages.error(
                                    request,
                                    (
                                        "Este e-mail já existe por favor"
                                        " digite um e-mail diferente!"
                                    ),
                                )
                                return redirect("/perfil-site/")

                            cpf_valida = re.compile(
                                "^(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2}|\d{3}\.?\d{3}\.?\d{3}-?\d{2})$"
                            )
                            busca = cpf_valida.search(cpf_cnpj)
                            if busca is None:
                                messages.error(
                                    request,
                                    (
                                        "Este formato de CPF ou CNPJ não é"
                                        " valido!"
                                    ),
                                )
                                return redirect("/perfil-site/")

                            r = re.compile(r"[^0-9]")
                            cpf_cnpj = r.sub("", cpf_cnpj)
                            if len(cpf_cnpj) == 11:
                                valida_cpf = is_cpf_valido(cpf_cnpj)
                                if valida_cpf is False:
                                    messages.error(
                                        request, "Este CPF não é valido!"
                                    )
                                    return redirect("/perfil-site/")
                            if len(cpf_cnpj) == 14:
                                valida_cnpj = is_cnpj_valido(cpf_cnpj)
                                if valida_cnpj is False:
                                    messages.error(
                                        request, "Este CNPJ não é valido!"
                                    )
                                    return redirect("/perfil-site/")

                            cpf_verifica = (
                                Cliente.objects.exclude(
                                    user_cliente_id=user.id
                                )
                                .filter(cpf_cnpj__iexact=cpf_cnpj)
                                .exists()
                            )
                            if cpf_verifica:
                                messages.error(
                                    request,
                                    (
                                        "Este CPF ou CNPJ já existe por favor"
                                        " digite um CPF ou CNPJ diferente!"
                                    ),
                                )
                                return redirect("/perfil-site/")

                            telefone = r.sub("", telefone)
                            data_nascimento = datetime.strptime(
                                data_nascimento, "%d/%m/%Y"
                            ).date()

                            if not (nr_casa and nr_casa.strip()):
                                nr_casa = None
                            else:
                                nr_casa = int(nr_casa)

                            cliente = Cliente.objects.filter(
                                user_cliente_id=user.id
                            ).first()
                            cliente_endereco = Endereco.objects.filter(
                                user_cliente_id=user.id
                            ).first()
                            if cliente:
                                user.first_name = nome
                                user.email = email
                                user.save()

                                cliente.telefone = telefone
                                cliente.cpf_cnpj = cpf_cnpj
                                cliente.data_nascimento = data_nascimento
                                cliente.save_base()

                                cliente_endereco.cep = cep
                                cliente_endereco.estado = estado
                                cliente_endereco.cidade = cidade
                                cliente_endereco.bairro = bairro
                                cliente_endereco.logradouro = logradouro
                                cliente_endereco.nr_casa = nr_casa
                                cliente_endereco.save()

                                messages.success(
                                    request, "Perfil editado com suecesso!"
                                )
                                return redirect("/perfil-site/")
                            else:
                                messages.error(
                                    request,
                                    (
                                        "Aconteuceu algum erro inesperado,"
                                        " favor tentar novamente!"
                                    ),
                                )
                                return redirect("/perfil-site/")
                        except Exception:
                            messages.error(
                                request,
                                (
                                    "Aconteceu algum erro insesperado favor"
                                    " tentar novamente!"
                                ),
                            )
                            return redirect("/perfil-site/")
                else:
                    response = {
                        "message": False,
                    }
                    return JsonResponse(
                        response, status=400, content_type="application/json"
                    )

            except Exception:
                response = {
                    "message": False,
                }
                return JsonResponse(
                    response, status=400, content_type="application/json"
                )


@login_required(login_url="/login")
def edit_password_site(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "POST":
            try:
                senha_atual = request.POST.get("password")
                senha_nova = request.POST.get("new_password")
                senha_nova_confirma = request.POST.get("confirm_password")

                if user.check_password(senha_atual):
                    if senha_nova == senha_nova_confirma:
                        user.set_password(senha_nova_confirma)
                        user.save()

                        messages.success(request, "Senha editada com sucesso!")
                        return redirect("/perfil-site/")
                    else:
                        messages.error(
                            request,
                            (
                                "A nova senha digitada não confere com a senha"
                                " digitada para confirmar!"
                            ),
                        )
                        return redirect("/perfil-site/")
                else:
                    messages.error(
                        request,
                        "Senha atual não confirma com o que foi digitado!",
                    )
                    return redirect("/perfil-site/")

            except Exception:
                messages.error(
                    request, "Senha não editada algum erro inesperado!"
                )
                return redirect("/perfil-site/")
