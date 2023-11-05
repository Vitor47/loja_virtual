from django.urls import path
from . import views

app_name = "admin.cliente"

urlpatterns = [
    path("cliente/", views.cliente, name="cliente"),
    path("search_cliente/", views.search_cliente, name="search_cliente"),
    path(
        "detalhes_cliente/<int:id>",
        views.detalhes_cliente,
        name="detalhes_cliente",
    ),
    path("ativo_inativo/<int:id>", views.ativo_inativo, name="ativo_inativo"),
]
