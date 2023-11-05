from django.urls import path
from . import views

app_name = "admin.dashboard"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
