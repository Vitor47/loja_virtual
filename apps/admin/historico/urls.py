from django.urls import path
from .views import historico

app_name = "admin.historico"

urlpatterns = [
    path("historico/", historico, name="historico"),
]
