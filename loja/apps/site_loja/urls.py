from django.urls import path
from ..site_loja.views import view_home, view_produto, view_conta, view_perfil, view_carrinho

app_name = 'site_loja'

urlpatterns = [
    path('', view_home.home, name='home'),
    path('produtos/', view_produto.produtos, name='produtos'),
    path('categoria-produto/<str:slug>', view_produto.categoria_produto, name='categoria_produto'),
    path('novidades/', view_produto.novidades, name='novidades'),
    path('ofertas/', view_produto.ofertas, name='ofertas'),
    path('detalhes-produto/<str:slug>', view_produto.detalhes_produto, name='detalhes_produto'),
    path('login/', view_conta.login, name='login'),
    path('logout/', view_conta.sair, name='sair'),
    path('criar-conta/', view_conta.create_count, name='create_count'),
    path('perfil-site/', view_perfil.perfil_site, name='perfil_site'),
    path('edit-password-site/', view_perfil.edit_password_site, name='edit_password_site'),
    path('adiciona-carrinho/', view_carrinho.adiciona_carrinho, name='adiciona_carrinho'),
    path('carrinho/', view_carrinho.carrinho, name='carrinho'),
    path('dados-perfil-carrinho/', view_carrinho.dados_perfil_carrinho, name='dados_perfil_carrinho'),
    path('frete-carrinho/', view_carrinho.frete_carrinho, name='frete_carrinho'),
    path('forma-pagamento-carrinho/', view_carrinho.forma_pagamento_carrinho, name='forma_pagamento_carrinho'),
    path('pagamento-carrinho/', view_carrinho.pagamento_carrinho, name='pagamento_carrinho'),
    path('gerar-pagamento/', view_carrinho.gerar_pagamento, name='gerar_pagamento'),
    ]