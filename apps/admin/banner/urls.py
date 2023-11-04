from django.urls import path
from . import views

app_name = "apps_administrador.banner"

urlpatterns = [
    path("banner/", views.banner, name="banner"),
    path("create_banner/", views.create_banner, name="create_banner"),
    path("edit_banner/<int:id>", views.edit_banner, name="edit_banner"),
    path("delete_banner/<int:id>", views.delete_banner, name="delete_banner"),
]
