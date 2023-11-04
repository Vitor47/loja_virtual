from django.urls import path
from . import views

app_name = "apps_administrador.configuracao"

urlpatterns = [
    path("configuracao/", views.configuracao, name="configuracao"),
    path("create_configuracao/", views.create_configuracao, name="create_configuracao"),
    path(
        "edit_configuracao/<int:id>", views.edit_configuracao, name="edit_configuracao"
    ),
    path(
        "delete_configuracao/<int:id>",
        views.delete_configuracao,
        name="delete_configuracao",
    ),
]
