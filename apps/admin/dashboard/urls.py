from django.urls import path
from . import views

app_name = "apps_administrador.dashboard"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
