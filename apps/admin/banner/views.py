# Cria Data Automático
from datetime import date

# Mensagens Template
from django.contrib import messages

# Atenticação de Login e Session
from django.contrib.auth.decorators import login_required, permission_required

# Retornar templates
from django.shortcuts import redirect, render

# Importa demais coisas
from django.contrib.auth.models import User

# Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

# Permissões
from ..decorators import manager_required

# Models
from .models import Banner


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("banner.view_banner")
def banner(request):
    banner = Banner.objects.all().order_by("-id")
    return render(request, "banner/index.html", {"banner": banner})


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("banner.add_banner")
def create_banner(request):
    if request.method == "GET":
        return render(request, "banner/create.html")
    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            image = request.FILES.get("image_banner")

            banner = Banner(
                imagem=image, status=True, user_cad=user, data_cad=date.today()
            )
            banner.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Banner).id,
                banner.id,
                f"ADD -> {banner.id}",
                ADDITION,
                "O banner %s foi cadastrado" % banner.id,
            )

            messages.success(request, "Banner cadastrado com sucesso!")
            return redirect("/admin/banner/")
        except Exception:
            messages.error(
                request, "Banner não cadastrado algum erro inesperado!"
            )
            return redirect("/admin/create_banner/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("banner.change_banner")
def edit_banner(request, id):
    item = Banner.objects.get(id=id)
    if request.method == "GET":
        return render(request, "banner/edit.html", {"banner": item})
    elif request.method == "POST":
        try:
            image = request.FILES.get("image_banner")
            status = request.POST.get("status")

            if image == None:
                item.imagem = item.imagem
            else:
                item.imagem = image

            if status == "1":
                item.status = True
            elif status == "2":
                item.status = False

            item.data_cad = item.data_cad
            item.dat_edit = date.today()
            item.user_cad = item.user_cad
            item.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Banner).id,
                item.id,
                f"EDIT -> {item.id}",
                CHANGE,
                "O banner %s foi editado" % item.id,
            )

            messages.success(request, "Banner editado com sucesso!")
            return redirect("/admin/banner/")
        except Exception:
            messages.error(
                request, "Banner não editado algum erro inesperado!"
            )
            return redirect(f"/admin/edit_banner/{id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("banner.change_banner")
def delete_banner(request, id):
    item = Banner.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(Banner).id,
            item.id,
            f"DELETE -> {item.id}",
            DELETION,
            "O banner %s foi deletado" % item.id,
        )

        item.delete()
        messages.success(request, "Banner deletado com sucesso!")
        return redirect("/admin/banner/")
