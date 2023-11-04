# Mensagens Template
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Retornar templates
from django.shortcuts import redirect, render

# Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

# Permissões
from ..decorators import manager_required

# Models
from .models import Configuracao


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("configuracao.view_configuracao")
def configuracao(request):
    if request.method == "GET":
        list_configs = Configuracao.objects.all().order_by("-id")
        return render(
            request, "configuracao/index.html", {"configuracao": list_configs}
        )


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("configuracao.create_configuracao")
def create_configuracao(request):
    if request.method == "GET":
        return render(request, "configuracao/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_configuracao")
            valor = request.POST.get("valor_configuracao")

            configuracao = Configuracao(
                nome=nome,
                valor=valor,
            )
            configuracao.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Configuracao).id,
                configuracao.id,
                f"ADD -> {configuracao.id}",
                ADDITION,
                "A configuração %s foi adicionada" % configuracao.id,
            )

            messages.success(request, "Configuração cadastrada com sucesso!")
            return redirect("/admin/configuracao/")
        except Exception as e:
            messages.error(
                request, "Configuração não cadastrada algum erro inesperado!"
            )
            return redirect("/admin/create_configuracao/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("configuracao.change_configuracao")
def edit_configuracao(request, id):
    item = Configuracao.objects.get(id=id)
    if request.method == "GET":
        return render(request, "configuracao/edit.html", {"configuracao": item})
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_configuracao")
            valor = request.POST.get("valor_configuracao")

            item.nome = nome
            item.valor = valor
            item.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Configuracao).id,
                item.id,
                f"EDIT -> {item.id}",
                CHANGE,
                "A configuração %s foi editada" % item.id,
            )

            messages.success(request, "Configuração editada com sucesso!")
            return redirect("/admin/configuracao/")
        except Exception as e:
            messages.error(request, "Configuração não editada algum erro inesperado!")
            return redirect(f"/admin/edit_configuracao/{id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("configuracao.delete_configuracao")
def delete_configuracao(request, id):
    item = Configuracao.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(Configuracao).id,
            item.id,
            f"DELETE -> {item.id}",
            DELETION,
            "A configuração %s foi deletada" % item.id,
        )

        item.delete()
        messages.success(request, "Configuração deletada com sucesso!")
        return redirect("/admin/configuracao/")
