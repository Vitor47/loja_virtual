from django.urls import path
from loja.apps.site_loja.views import view_home, view_produto, view_conta

app_name = 'site_loja'

urlpatterns = [
    path('', view_home.home, name='home'),
    path('produtos/', view_produto.produtos, name='produtos'),
    path('detalhes-produto/', view_produto.detalhes_produto, name='detalhes_produto'),
    path('login/', view_conta.login, name='login'),
    ]