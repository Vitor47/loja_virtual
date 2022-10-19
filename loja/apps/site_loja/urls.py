from django.urls import path
from . import views

app_name = 'site_loja'

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('detalhes-produto/', views.detalhes_produto, name='detalhes_produto'),
    path('login/', views.login, name='login'),
    path('criar-conta/', views.create_count, name='create_count'),
    ]