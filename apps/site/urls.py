from django.urls import path

from .views import carrinho, conta, home, perfil
from .views import produto

app_name = "site"

urlpatterns = [
    path("", home.home, name="home"),
    path("produtos/", produto.produtos, name="produtos"),
    path(
        "categoria-produto/<str:slug>",
        produto.categoria_produto,
        name="categoria_produto",
    ),
    path("novidades/", produto.novidades, name="novidades"),
    path("ofertas/", produto.ofertas, name="ofertas"),
    path(
        "detalhes-produto/<str:slug>", produto.detalhes_produto, name="detalhes_produto"
    ),
    path("login/", conta.login, name="login"),
    path("logout/", conta.sair, name="sair"),
    path("criar-conta/", conta.create_count, name="create_count"),
    path("perfil-site/", perfil.perfil_site, name="perfil_site"),
    path("edit-password-site/", perfil.edit_password_site, name="edit_password_site"),
    path("adiciona-carrinho/", carrinho.adiciona_carrinho, name="adiciona_carrinho"),
    path("carrinho/", carrinho.carrinho, name="carrinho"),
    path(
        "dados-perfil-carrinho/",
        carrinho.dados_perfil_carrinho,
        name="dados_perfil_carrinho",
    ),
    path("frete-carrinho/", carrinho.frete_carrinho, name="frete_carrinho"),
    path(
        "forma-pagamento-carrinho/",
        carrinho.forma_pagamento_carrinho,
        name="forma_pagamento_carrinho",
    ),
    path("pagamento-carrinho/", carrinho.pagamento_carrinho, name="pagamento_carrinho"),
    path("gerar-pagamento/", carrinho.gerar_pagamento, name="gerar_pagamento"),
]
