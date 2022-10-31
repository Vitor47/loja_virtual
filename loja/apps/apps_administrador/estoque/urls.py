from django.urls import path
from . import views

app_name = 'apps_administrador.estoque'

urlpatterns = [
    path('estoque/', views.estoque, name='estoque'),
    ]
