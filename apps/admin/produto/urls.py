from django.urls import path
from . import views

app_name = "apps_administrador.produto"

urlpatterns = [
    path("produto/", views.produto, name="produto"),
    path("search_produto/", views.search_produto, name="search_produto"),
    path("create_produto/", views.create_produto, name="create_produto"),
    path("edit_produto/<int:id>", views.edit_produto, name="edit_produto"),
    path("delete_produto/<int:id>", views.delete_produto, name="delete_produto"),
    path(
        "delete_image_produto/<int:id>",
        views.delete_image_produto,
        name="delete_image_produto",
    ),
    path("categoria_produto/", views.categoria_produto, name="categoria_produto"),
    path(
        "create_categoria_produto/",
        views.create_categoria_produto,
        name="create_categoria_produto",
    ),
    path(
        "edit_categoria_produto/<int:id>",
        views.edit_categoria_produto,
        name="edit_categoria_produto",
    ),
    path(
        "delete_categoria_produto/<int:id>",
        views.delete_categoria_produto,
        name="delete_categoria_produto",
    ),
    path("atributo_produto/", views.atributo_produto, name="atributo_produto"),
    path(
        "create_atributo_produto/",
        views.create_atributo_produto,
        name="create_atributo_produto",
    ),
    path(
        "edit_atributo_produto/<int:id>",
        views.edit_atributo_produto,
        name="edit_atributo_produto",
    ),
    path(
        "delete_atributo_produto/<int:id>",
        views.delete_atributo_produto,
        name="delete_atributo_produto",
    ),
    path(
        "produto_atributo_produto/<int:id>",
        views.produto_atributo_produto,
        name="produto_atributo_produto",
    ),
    path("diametro_produto/", views.diametro_produto, name="diametro_produto"),
    path(
        "create_diametro_produto/",
        views.create_diametro_produto,
        name="create_diametro_produto",
    ),
    path(
        "edit_diametro_produto/<int:id>",
        views.edit_diametro_produto,
        name="edit_diametro_produto",
    ),
    path(
        "delete_diametro_produto/<int:id>",
        views.delete_diametro_produto,
        name="delete_diametro_produto",
    ),
    path(
        "produto_diametro_produto/<int:id>",
        views.produto_diametro_produto,
        name="produto_diametro_produto",
    ),
]
