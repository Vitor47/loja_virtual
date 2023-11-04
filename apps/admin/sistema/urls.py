from django.urls import path
from . import views

app_name = "apps_administrador.sistema"

urlpatterns = [
    path("", views.login, name="login"),
    path("perfil/", views.perfil, name="perfil"),
    path("senha/", views.senha, name="senha"),
    path("sair/", views.sair, name="sair"),
    path("usuario/", views.list_user, name="list_user"),
    path("create_user/", views.create_user, name="create_user"),
    path("edit_user/<int:id>", views.edit_user, name="edit_user"),
    path("delete_user/<int:id>", views.delete_user, name="delete_user"),
    path("grupo_acesso/", views.grupo_acesso, name="grupo_acesso"),
    path("create_grupo_acesso/", views.create_grupo_acesso, name="create_grupo_acesso"),
    path(
        "edit_grupo_acesso/<int:id>", views.edit_grupo_acesso, name="edit_grupo_acesso"
    ),
    path(
        "delete_grupo_acesso/<int:id>",
        views.delete_grupo_acesso,
        name="delete_grupo_acesso",
    ),
    path(
        "add_users_group/<int:id_group>", views.add_users_group, name="add_users_group"
    ),
    path(
        "add_permission_group/<int:id_group>",
        views.add_permission_group,
        name="add_permission_group",
    ),
]
