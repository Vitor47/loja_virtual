# Mensagens Template
from django.contrib import messages

# Atenticação de Login e Session
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required

# Cripto senhas
from django.contrib.auth.hashers import make_password

# Retornar templates
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse

# Importa demais coisas
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Q

# Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

# Permissões
from ..decorators import manager_required
from .models import Auditoria


def login(request):
    if request.method == "GET":
        return render(request, "login/index.html")
    else:
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        user = authenticate(username=username, password=senha)
        if user:
            if (
                user.is_staff == True
                or user.is_superuser == True
                and user.is_active == True
            ):
                login_django(request, user)

                LogEntry.objects.log_action(
                    request.user.id,
                    ContentType.objects.get_for_model(User).id,
                    user.id,
                    f"LOG -> {user.id}",
                    CHANGE,
                    "O Usuário %s logou no sistema" % user.id,
                )

                ip = request.META.get("REMOTE_ADDR")
                request.session["ip"] = ip

                auditoria = Auditoria(
                    user=user,
                    mensagem="LOGOU NO SISTEMA",
                    ip=f"CLIENTE IP -> {ip}",
                )
                auditoria.save()

                return redirect("/admin/dashboard/")
            else:
                messages.error(request, "Usuário não tem permissão!")
                return redirect("/admin")
        else:
            messages.error(request, "Usuário ou senha incorretos!")
            return redirect("/admin")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
def perfil(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            return render(request, "perfil/index.html", {"usuario": user})
        elif request.method == "POST":
            try:
                if user:
                    nome = request.POST.get("nome_usuario")
                    username = request.POST.get("usuario")
                    email = request.POST.get("email_usuario")

                    user_name = (
                        User.objects.exclude(id=user.id)
                        .filter(username__iexact=username)
                        .exists()
                    )
                    if user_name:
                        messages.error(
                            request,
                            "Este usuário já existe por favor digite um usuário diferente!",
                        )
                        return redirect("/admin/perfil/")

                    email_verifica = (
                        User.objects.exclude(id=user.id)
                        .filter(email__iexact=email)
                        .exists()
                    )
                    if email_verifica:
                        messages.error(
                            request,
                            "Este E-mail já existe por favor digite um e-mail diferente!",
                        )
                        return redirect("/admin/perfil/")

                    user.first_name = nome
                    user.username = username
                    user.email = email
                    user.save()

                    LogEntry.objects.log_action(
                        request.user.id,
                        ContentType.objects.get_for_model(User).id,
                        user.id,
                        f"EDIT -> {user.first_name + '-' + user.username + '-' + user.email}",
                        CHANGE,
                        "O Usuário com id -> %s alterou o perfil" % user.id,
                    )

                    messages.success(request, "Perfil editado com sucesso!")
                    return redirect("/admin/dashboard/")
                else:
                    messages.error(request, "Perfil não encontrado!")
                    return redirect("/admin/perfil/")

            except Exception as e:
                messages.error(request, "Perfil não editado algum erro inesperado!")
                return redirect("/admin/perfil/")
    else:
        return redirect("/admin")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
def senha(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            return render(request, "perfil/senha.html", {"usuario": user})
        elif request.method == "POST":
            try:
                if user:
                    senha_atual = request.POST.get("senha_atual_usuario")
                    senha_nova = request.POST.get("nova_senha_usuario")
                    senha_nova_confirma = request.POST.get(
                        "confirmar_nova_senha_usuario"
                    )

                    if user.check_password(senha_atual):
                        if senha_nova == senha_nova_confirma:
                            user.set_password(senha_nova_confirma)
                            user.save()

                            LogEntry.objects.log_action(
                                request.user.id,
                                ContentType.objects.get_for_model(User).id,
                                user.id,
                                f"EDIT -> {user.id}",
                                CHANGE,
                                "O Usuário %s alterou a senha" % user.id,
                            )

                            messages.success(request, "Senha editada com sucesso!")
                            return redirect("/admin/dashboard/")
                        else:
                            messages.error(
                                request,
                                "A nova senha digitada não confere com a senha digitada para confirmar!",
                            )
                            return redirect("/admin/senha/")
                    else:
                        messages.error(
                            request, "Senha atual não confirma com o que foi digitado!"
                        )
                        return redirect("/admin/senha/")
                else:
                    messages.error(request, "Perfil não encontrado!")
                    return redirect("/admin/dashboard/")

            except Exception as e:
                messages.error(request, "Senha não editada algum erro inesperado!")
                return redirect("/admin/senha/")
    else:
        return redirect("/admin")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
def sair(request):
    logout(request)
    return redirect("/admin")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("user.view_user")
def list_user(request):
    if request.method == "GET":
        list_users = User.objects.filter(is_staff=True).order_by("-id")
        return render(request, "usuarios/index.html", {"users": list_users})


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("user.add_user")
def create_user(request):
    if request.method == "GET":
        return render(request, "usuarios/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_user")
            sobrenome = request.POST.get("sobrenome_user")
            username = request.POST.get("username_user")
            email = request.POST.get("email_user")
            senha = request.POST.get("senha_user")
            confirmar_senha_user = request.POST.get("confirmar_senha_user")
            super_admin = request.POST.get("super_admin")
            membro_equipe = request.POST.get("membro_equipe")

            usuario_username = User.objects.filter(username__iexact=username).exists()
            if usuario_username:
                messages.error(
                    request, "Erro! Já existe um usuário com o mesmo username!"
                )
                return redirect("/admin/create_user/")

            usuario_email = User.objects.filter(email__iexact=email).exists()
            if usuario_email:
                messages.error(request, "Erro! Já existe um usuário com o mesmo email!")
                return redirect("/admin/create_user/")

            if senha != confirmar_senha_user:
                return redirect("/admin/create_user/")
            else:
                if super_admin != None:
                    super_admin = True
                    membro_equipe = True
                else:
                    super_admin = False
                    membro_equipe = False

                if membro_equipe != None:
                    membro_equipe = True
                    super_admin = False
                else:
                    membro_equipe = False
                    super_admin = False

            user = User(
                first_name=nome,
                last_name=sobrenome,
                username=username,
                email=email,
                password=make_password(senha),
                is_active=True,
                is_staff=membro_equipe,
                is_superuser=super_admin,
            )
            user.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(User).id,
                user.id,
                f"ADD -> {user.username + '-' + user.email}",
                ADDITION,
                "O usuário %s foi adicionado" % user.id,
            )

            messages.success(request, "Usuário criado com sucesso!")
            return redirect("/admin/usuario/")
        except Exception as e:
            messages.error(request, "Usuário não criado algum erro inesperado!")
            return redirect("/admin/create_user/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("user.change_user")
def edit_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "GET":
        if user.username == "vitor.miolo" or user.email == "vitormateusmiolo@gmail.com":
            messages.error(request, "Você não tem acesso para editar esse usuário!")
            return redirect("/admin/usuario/")

        return render(request, "usuarios/edit.html", {"user": user})
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_user")
            sobrenome = request.POST.get("sobrenome_user")
            username = request.POST.get("username_user")
            email = request.POST.get("email_user")
            senha = request.POST.get("senha_user")
            confirmar_senha_user = request.POST.get("confirmar_senha_user")
            super_admin = request.POST.get("super_admin")
            membro_equipe = request.POST.get("membro_equipe")
            status = request.POST.get("status")

            if status == "1":
                status = True
            elif status == "2":
                status = False

            usuario_username = (
                User.objects.exclude(id=user.id)
                .filter(username__iexact=username)
                .exists()
            )
            if usuario_username:
                messages.error(
                    request, "Erro! Já existe um usuário com o mesmo username!"
                )
                return redirect(f"/admin/edit_user/{id}")

            usuario_email = (
                User.objects.exclude(id=user.id).filter(email__iexact=email).exists()
            )
            if usuario_email:
                messages.error(request, "Erro! Já existe um usuário com o mesmo email!")
                return redirect(f"/admin/edit_user/{id}")

            if senha != confirmar_senha_user:
                return redirect(f"/admin/edit_user/{id}")
            else:
                if super_admin != None:
                    super_admin = True
                    membro_equipe = True
                else:
                    super_admin = False
                    membro_equipe = False

                if membro_equipe != None:
                    membro_equipe = True
                    super_admin = False
                else:
                    membro_equipe = False
                    super_admin = False

                user.first_name = nome
                user.last_name = sobrenome
                user.username = username
                user.email = email
                user.set_password(senha)
                user.is_active = status
                user.is_staff = membro_equipe
                user.is_superuser = super_admin
                user.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(User).id,
                user.id,
                f"EDITOU -> {user.username + '-' + user.email}",
                CHANGE,
                "O usuário %s foi editado" % user.id,
            )

            messages.success(request, "Usuário editado com sucesso!")
            return redirect("/admin/usuario/")
        except Exception as e:
            messages.error(request, "Usuário não editado algum erro inesperado!")
            return redirect(f"/admin/edit_user/{id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("user.delete_user")
def delete_user(request, id):
    item = User.objects.get(id=id)
    if request.method == "GET":
        if item.username == "vitor.miolo" or item.email == "vitormateusmiolo@gmail.com":
            messages.error(request, "Você não tem acesso para deletar esse usuário!")
            return redirect("/admin/usuario/")

        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(User).id,
            item.id,
            f"DELETE -> {item.id}",
            DELETION,
            "O usuário %s foi deletado" % item.id,
        )

        item.delete()

        messages.success(request, "Usuário deletado com sucesso!")
        return redirect("/admin/usuario/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("group.view_group")
def grupo_acesso(request):
    if request.method == "GET":
        groups = Group.objects.all().order_by("-id")
        return render(request, "grupo_acesso/index.html", {"groups": groups})


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("group.add_group")
def create_grupo_acesso(request):
    if request.method == "GET":
        return render(request, "grupo_acesso/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_group")
            name = Group.objects.filter(name__iexact=nome).exists()
            if name:
                messages.error(request, "Erro! Já existe um grupo com o mesmo nome!")
                return redirect("/admin/create_grupo_acesso/")

            group = Group(
                name=nome,
            )
            group.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Group).id,
                group.id,
                f"ADD -> {group.name}",
                ADDITION,
                "O grupo %s foi adicionado" % group.id,
            )

            messages.success(request, "Grupo criado com sucesso!")
            return redirect("/admin/grupo_acesso/")
        except Exception as e:
            messages.error(request, "Grupo não criado algum erro inesperado!")
            return redirect(f"/admin/grupo_acesso/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("group.change_group")
def edit_grupo_acesso(request, id):
    group = Group.objects.get(id=id)
    if request.method == "GET":
        return render(request, "grupo_acesso/edit.html", {"group": group})
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_group")
            name = (
                Group.objects.exclude(name=group.name)
                .filter(name__iexact=nome)
                .exists()
            )
            if name:
                messages.error(request, "Erro! Já existe um grupo com o mesmo nome!")
                return redirect(f"/admin/edit_grupo_acesso/{id}")

            group.name = nome
            group.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Group).id,
                group.id,
                f"EDIT -> {group.name}",
                CHANGE,
                "O grupo %s foi editado" % group.id,
            )

            messages.success(request, "O grupo foi editado com sucesso!")
            return redirect("/admin/grupo_acesso/")
        except Exception as e:
            messages.error(request, "O grupo não foi editado algum erro inesperado!")
            return redirect(f"/admin/edit_grupo_acesso/{id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("group.change_group")
def delete_grupo_acesso(request, id):
    if request.method == "GET":
        group = Group.objects.get(id=id)
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(Group).id,
            group.id,
            f"DELETE -> {group.name}",
            DELETION,
            "O grupo %s foi deletado" % group.id,
        )

        group.delete()
        messages.success(request, "O grupo foi deletado com sucesso!")
        return redirect("/admin/grupo_acesso/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("group.add_group")
def add_users_group(request, id_group):
    users = (
        User.objects.exclude(Q(is_superuser=True))
        .filter(Q(is_staff=True), Q(is_active=True))
        .order_by("-id")
    )
    grupo = Group.objects.get(id=id_group)
    users_in_group = grupo.user_set.all()
    marcado = False
    if request.method == "GET":
        usuarios = []
        for user in users:
            for user_in_group in users_in_group:
                if user.id == user_in_group.id:
                    marcado = True
                    break
                else:
                    marcado = False

            usuario = {
                "id": user.id,
                "nome": user.first_name + " " + user.last_name,
                "usuario": user.username,
                "marcado": marcado,
            }
            usuarios.append(usuario)

        context = {}
        context["usuarios"] = usuarios
        context["grupo"] = grupo
        return TemplateResponse(request, "grupo_acesso/users.html", context)
    elif request.method == "POST":
        try:
            list_id_users = request.POST.getlist("user_id[]")
            list_users = (
                User.objects.all()
                .exclude(is_superuser=True)
                .filter(is_staff=True)
                .values_list(flat=True)
                .order_by("-id")
            )
            for i in list_users:
                user = User.objects.get(id=i)
                group = Group.objects.get(id=id_group)
                group.user_set.remove(user)

            for y in list_id_users:
                user = User.objects.get(id=y)
                group = Group.objects.get(id=id_group)
                user.groups.add(group)

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Group).id,
                grupo.id,
                f"ADD ->",
                ADDITION,
                "Os Usuários foram adicionados ao grupo %s" % grupo.id,
            )

            messages.success(
                request, "Usuários foram adicionados ao grupo com sucesso!"
            )
            return redirect("/admin/grupo_acesso/")
        except Exception as e:
            messages.error(
                request,
                "Usuários não foram adicionados ao grupo algum erro inesperado!",
            )
            return redirect("/admin/grupo_acesso/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("group.add_group")
def add_permission_group(request, id_group):
    grupo = Group.objects.get(id=id_group)
    content_type_ids = []
    content_type_ids.append(ContentType.objects.get(model="user").id)
    content_type_ids.append(ContentType.objects.get(model="permission").id)
    content_type_ids.append(ContentType.objects.get(model="group").id)
    content_type_ids.append(ContentType.objects.get(model="session").id)
    content_type_ids.append(ContentType.objects.get(model="contenttype").id)
    content_type_ids.append(ContentType.objects.get(model="logentry").id)
    content_type_ids.append(ContentType.objects.get(model="auditoria").id)
    content_type_ids.append(ContentType.objects.get(model="produtoimagens").id)
    content_type_ids.append(ContentType.objects.get(model="endereco").id)
    content_type_ids.append(ContentType.objects.get(model="produtoatributoproduto").id)
    content_type_ids.append(ContentType.objects.get(model="produtodiamentroproduto").id)
    permissoes = Permission.objects.exclude(content_type_id__in=content_type_ids)
    if request.method == "GET":
        table_relacionada = grupo.permissions.all().order_by("-id")
        permissions = []
        marcado = False
        for permissao in permissoes:
            for item in table_relacionada:
                if item.name == permissao.name:
                    marcado = True
                    break
                else:
                    marcado = False

            permissao = {
                "id": permissao.id,
                "name": permissao.name,
                "marcado": marcado,
            }
            permissions.append(permissao)

        context = {}
        context["permissoes"] = permissions
        context["table_relacionada"] = table_relacionada
        context["grupo"] = grupo
        return TemplateResponse(request, "grupo_acesso/permissions.html", context)
    elif request.method == "POST":
        try:
            list_id_permissions = request.POST.getlist("permissao_id[]")
            list_permissions = (
                Permission.objects.all().values_list(flat=True).order_by("-id")
            )
            for i in list_permissions:
                permission = Permission.objects.get(id=i)
                grupo = Group.objects.get(id=id_group)
                grupo.permissions.remove(permission)

            for y in list_id_permissions:
                permission = Permission.objects.get(id=y)
                grupo = Group.objects.get(id=id_group)
                grupo.permissions.add(permission)

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Group).id,
                grupo.id,
                f"ADD -> {grupo.name}",
                ADDITION,
                "As permissões foram adicionadas ao grupo",
            )

            messages.success(request, "As permissões foram adicionadas ao grupo!")
            return redirect("/admin/grupo_acesso/")
        except Exception as e:
            messages.error(
                request, "As permissões não foram criadas algum erro inesperado!"
            )
            return redirect(f"/admin/grupo_acesso/")
