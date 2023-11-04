from apps.admin.produto.models import Produto, ProdutoCategoria
from apps.admin.banner.models import Banner
from django.template.response import TemplateResponse


def home(request):
    if request.method == "GET":
        banners = Banner.objects.filter(status=True).order_by("-id")
        categorias_produtos = ProdutoCategoria.objects.all().order_by("-id")
        ofertas = (
            Produto.objects.filter(tipo_id=1, status=True)
            .exclude(quantidade=0)
            .order_by("-id")[:10]
        )
        novidades = (
            Produto.objects.filter(tipo_id=2, status=True)
            .exclude(quantidade=0)
            .order_by("-id")[:10]
        )

        offers = []
        for oferta in ofertas:
            if oferta.desconto is not None and oferta.desconto != "":
                valor_com_desconto = oferta.valor - oferta.desconto
                percent_descont = 100 - (
                    (float(valor_com_desconto) * 100) // float(oferta.valor)
                )
            else:
                valor_com_desconto = None
                percent_descont = None

            oferta = {
                "id": oferta.id,
                "nome": oferta.nome,
                "imagem_principal": oferta.imagem_principal,
                "valor_inicial": oferta.valor,
                "valor_com_desconto": valor_com_desconto,
                "percent_desconto": percent_descont,
                "slug": oferta.slug,
            }
            offers.append(oferta)

        news = []
        for novidade in novidades:
            if novidade.desconto is not None and novidade.desconto != "":
                valor_com_desconto = novidade.valor - novidade.desconto
                percent_descont = 100 - (
                    (float(valor_com_desconto) * 100) // float(novidade.valor)
                )
            else:
                valor_com_desconto = None
                percent_descont = None

            novidade = {
                "id": novidade.id,
                "nome": novidade.nome,
                "imagem_principal": novidade.imagem_principal,
                "valor_inicial": novidade.valor,
                "valor_com_desconto": valor_com_desconto,
                "percent_desconto": percent_descont,
                "slug": novidade.slug,
            }
            news.append(novidade)

        context = {}
        context["banners"] = banners
        context["categorias_produtos"] = categorias_produtos
        context["ofertas"] = offers
        context["tamanho_array_oferta"] = len(offers)
        context["tamanho_array_novidade"] = len(news)
        context["novidades"] = news
        return TemplateResponse(request, "home/index.html", context)
