# Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Cria Data Automático
from datetime import date

# Imagens
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import uuid

# Mensagens Template
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Retornar templates
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse

# Importa demais coisas
from django.contrib.auth.models import User
from slug import slug

# Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

# Decimal
from decimal import Decimal

# Forms
from .forms import FormCodigoServico, FormCodigoFormato

# Models
from .models import (
    Produto,
    ProdutoAtributo,
    ProdutoCategoria,
    ProdutoImagens,
    ProdutoTipo,
    ProdutoAtributoProduto,
    ProdutoDiamentro,
    ProdutoDiamentroProduto,
)

# Permissões
from ..decorators import manager_required


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.view_produto")
def produto(request):
    list_products = Produto.objects.all().order_by("-id")
    paginator = Paginator(list_products, 10)
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "produto/index.html", {"produtos": products})


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.view_produto")
def search_produto(request):
    list_products = Produto.objects.all().order_by("-id")
    consulta_nome = request.GET.get("pesquisar_por_nome")
    if consulta_nome is not None:
        list_products = list_products.filter(nome__icontains=consulta_nome)
    paginator = Paginator(list_products, 10)
    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "produto/index.html", {"produtos": products})


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.add_produto")
def create_produto(request):
    if request.method == "GET":
        list_tipos = ProdutoTipo.objects.all()
        list_categoria = ProdutoCategoria.objects.all()
        return render(
            request,
            "produto/create.html",
            {"tipos": list_tipos, "categorias": list_categoria},
        )
    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            nome = request.POST.get("nome_produto")
            valor = request.POST.get("valor_produto")
            quantidade = request.POST.get("quantidade_produto")
            image = request.FILES.get("image_produto")
            descricao = request.POST.get("descricao_produto")
            desconto = request.POST.get("desconto_produto")
            tipo = request.POST.get("tipo_produto")
            categoria = request.POST.get("categoria_produto")

            valor_formatado = (
                valor.replace("R$:", "").replace(".", "").replace(",", ".")
            )
            if desconto is not None and desconto != "":
                valor_formatado_desconto = (
                    desconto.replace("R$:", "").replace(".", "").replace(",", ".")
                )
            else:
                valor_formatado_desconto = None

            if image.size < 500000:
                name = f"{uuid.uuid4()}.jpg"
                img = Image.open(image)
                img = img.convert("RGB")
                img = img.resize((1024, 1024))
                output = BytesIO()
                img.save(output, format="JPEG", quality=100)
                output.seek(0)
                img_final = InMemoryUploadedFile(
                    output,
                    "ImageField",
                    name,
                    "image/jpeg",
                    sys.getsizeof(output),
                    None,
                )
            else:
                messages.error(
                    request, "Imagem com tamanho não permitido o limite é 500kb!"
                )
                return redirect("/admin/create_produto/")

            produto = Produto(
                nome=nome,
                slug=slug(nome),
                valor=valor_formatado,
                quantidade=int(quantidade),
                imagem_principal=img_final,
                desconto=valor_formatado_desconto,
                status=True,
                categoria_id=int(categoria),
                tipo_id=int(tipo),
                descricao=descricao,
                user_cad=user,
                data_cad=date.today(),
            )
            produto.save()

            produto.slug = slug(produto.nome) + "_" + str(produto.id)
            produto.save()

            list_imagens = request.FILES.getlist("imagens_produto[]", None)
            for image in list_imagens:
                if image is not None:
                    if image.size < 500000:
                        name = f"{uuid.uuid4()}.jpg"
                        img = Image.open(image)
                        img = img.convert("RGB")
                        img = img.resize((1024, 1024))
                        output = BytesIO()
                        img.save(output, format="JPEG", quality=100)
                        output.seek(0)
                        img_final = InMemoryUploadedFile(
                            output,
                            "ImageField",
                            name,
                            "image/jpeg",
                            sys.getsizeof(output),
                            None,
                        )

                        produto_imagem = ProdutoImagens(
                            imagem=img_final,
                            produto_id=produto.id,
                            user_cad=user,
                            data_cad=date.today(),
                        )
                        produto_imagem.save()
                    else:
                        messages.error(
                            request,
                            "Imagem com tamanho não permitido o limite é 500kb!",
                        )
                        return redirect("/admin/create_produto/")

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Produto).id,
                produto.id,
                f"ADD -> {produto.id}",
                ADDITION,
                "O produto %s foi adicionado" % produto.id,
            )

            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect("/admin/produto/")
        except Exception:
            messages.error(request, "Produto não cadastrado algum erro inesperado!")
            return redirect("/admin/create_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.change_produto")
def edit_produto(request, id):
    item = Produto.objects.get(id=id)
    list_tipos = ProdutoTipo.objects.all()
    list_categoria = ProdutoCategoria.objects.all()
    list_imagens = ProdutoImagens.objects.filter(produto_id=id)
    if request.method == "GET":
        return render(
            request,
            "produto/edit.html",
            {
                "produto": item,
                "tipos": list_tipos,
                "categorias": list_categoria,
                "imagens": list_imagens,
            },
        )
    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            nome = request.POST.get("nome_produto")
            status = request.POST.get("status")
            valor = request.POST.get("valor_produto")
            quantidade = request.POST.get("quantidade_produto")
            image = request.FILES.get("image_produto")
            descricao = request.POST.get("descricao_produto")
            desconto = request.POST.get("desconto_produto")
            tipo = request.POST.get("tipo_produto")
            categoria = request.POST.get("categoria_produto")

            valor_formatado = (
                valor.replace("R$:", "").replace(".", "").replace(",", ".")
            )
            if desconto is not None and desconto != "":
                valor_formatado_desconto = (
                    desconto.replace("R$:", "").replace(".", "").replace(",", ".")
                )
            else:
                valor_formatado_desconto = None

            if image == None:
                item.imagem_principal = item.imagem_principal
            else:
                if image.size < 500000:
                    name = f"{uuid.uuid4()}.jpg"
                    img = Image.open(image)
                    img = img.convert("RGB")
                    img = img.resize((1024, 1024))
                    output = BytesIO()
                    img.save(output, format="JPEG", quality=100)
                    output.seek(0)
                    img_final = InMemoryUploadedFile(
                        output,
                        "ImageField",
                        name,
                        "image/jpeg",
                        sys.getsizeof(output),
                        None,
                    )
                else:
                    messages.error(
                        request, "Imagem com tamanho não permitido o limite é 500kb!"
                    )
                    return redirect("/admin/create_produto/")

                item.imagem_principal = img_final

            if status == "1":
                item.status = True
            elif status == "2":
                item.status = False

            item.nome = nome
            item.slug = slug(nome) + "_" + str(id)
            item.valor = valor_formatado
            item.quantidade = int(quantidade)
            item.desconto = valor_formatado_desconto
            item.tipo_id = int(tipo)
            item.categoria_id = int(categoria)
            item.descricao = descricao
            item.data_cad = item.data_cad
            item.user_cad = item.user_cad
            item.dat_edit = date.today()
            item.save()

            list_imagens = request.FILES.getlist("imagens_produto[]", None)
            for image in list_imagens:
                if image is not None:
                    if image.size < 500000:
                        name = f"{uuid.uuid4()}.jpg"
                        img = Image.open(image)
                        img = img.convert("RGB")
                        img = img.resize((1024, 1024))
                        output = BytesIO()
                        img.save(output, format="JPEG", quality=100)
                        output.seek(0)
                        img_final = InMemoryUploadedFile(
                            output,
                            "ImageField",
                            name,
                            "image/jpeg",
                            sys.getsizeof(output),
                            None,
                        )

                        produto_imagem = ProdutoImagens(
                            imagem=img_final,
                            produto_id=item.id,
                            user_cad=user,
                            data_cad=date.today(),
                        )
                        produto_imagem.save()
                    else:
                        messages.error(
                            request,
                            "Imagem com tamanho não permitido o limite é 500kb!",
                        )
                        return redirect("/admin/create_produto/")

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(Produto).id,
                item.id,
                f"EDIT -> {item.id}",
                CHANGE,
                "O produto %s foi editado" % item.id,
            )

            messages.success(request, "Produto editado com sucesso!")
            return redirect("/admin/produto/")
        except Exception as e:
            messages.error(request, "Produto não editado algum erro inesperado!")
            return redirect(f"/admin/edit_produto/{id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.delete_produto")
def delete_produto(request, id):
    item = Produto.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(Produto).id,
            item.id,
            f"DELETE -> {item.id}",
            DELETION,
            "O produto %s foi deletado" % item.id,
        )

        item.delete()
        messages.success(request, "Produto deletado com sucesso!")
        return redirect("/admin/produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.delete_produto")
def delete_image_produto(request, id):
    item = ProdutoImagens.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(ProdutoImagens).id,
            item.id,
            f"DELETE -> {item.id}",
            DELETION,
            "A imagem do produto %s foi deletado" % item.id,
        )

        item.delete()

        messages.success(request, "Imagem deletada com sucesso!")
        return redirect(f"/admin/edit_produto/{item.produto_id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.view_produtocategoria")
def categoria_produto(request):
    if request.method == "GET":
        categorias = ProdutoCategoria.objects.all().order_by("-id")
        return render(
            request, "produto/categoria/index.html", {"categorias": categorias}
        )


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.add_produtocategoria")
def create_categoria_produto(request):
    if request.method == "GET":
        return render(request, "produto/categoria/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_categoria")
            icone = request.POST.get("icone_categoria")
            categoria = ProdutoCategoria(nome=nome, icone=icone, slug=slug(nome))
            categoria.save()

            categoria.slug = slug(categoria.nome) + "_" + str(categoria.id)
            categoria.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoCategoria).id,
                categoria.id,
                f"ADD -> {categoria.id}",
                ADDITION,
                "A categoria %s foi adicionada" % categoria.id,
            )

            messages.success(request, "Categoria adicionada com sucesso!")
            return redirect("/admin/categoria_produto/")
        except Exception as e:
            messages.error(
                request, "Categoria não adicionada aconteceu algum erro inesperado!"
            )
            return redirect("/admin/categoria_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.change_produtocategoria")
def edit_categoria_produto(request, id):
    categoria = ProdutoCategoria.objects.get(id=id)
    if request.method == "GET":
        return render(request, "produto/categoria/edit.html", {"categoria": categoria})
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_categoria")
            icone = request.POST.get("icone_categoria")

            categoria.nome = nome
            categoria.icone = icone
            categoria.slug = slug(categoria.nome) + "_" + str(categoria.id)
            categoria.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoCategoria).id,
                categoria.id,
                f"EDIT -> {categoria.id}",
                CHANGE,
                "A categoria %s editado" % categoria.id,
            )

            messages.success(request, "Categoria editada com sucesso!")
            return redirect("/admin/categoria_produto/")
        except Exception as e:
            messages.error(
                request, "Categoria não editada aconteceu algum erro inesperado!"
            )
            return redirect("/admin/categoria_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.delete_produtocategoria")
def delete_categoria_produto(request, id):
    categoria = ProdutoCategoria.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(ProdutoAtributo).id,
            categoria.id,
            f"DELETE -> {categoria.id}",
            DELETION,
            "A categoria %s foi deletada" % categoria.id,
        )

        categoria.delete()

        messages.success(request, "A categoria foi deletada!")
        return redirect("/admin/categoria_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.view_produtoatributo")
def atributo_produto(request):
    atributos = ProdutoAtributo.objects.all().order_by("-id")
    if request.method == "GET":
        paginator = Paginator(atributos, 10)
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            page = 1
        try:
            list_atributos = paginator.page(page)
        except (EmptyPage, InvalidPage):
            list_atributos = paginator.page(paginator.num_pages)
        return render(
            request, "produto/atributo/index.html", {"atributos": list_atributos}
        )


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.add_produtoatributo")
def create_atributo_produto(request):
    if request.method == "GET":
        return render(request, "produto/atributo/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_atributo")
            valor = request.POST.get("valor_atributo")
            atributo = ProdutoAtributo(
                nome=nome,
                valor=valor,
            )
            atributo.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoAtributo).id,
                atributo.id,
                f"ADD -> {atributo.id}",
                ADDITION,
                "O Atributo %s foi adicionado" % atributo.id,
            )

            messages.success(request, "Atributo adicionado com sucesso!")
            return redirect("/admin/atributo_produto/")
        except Exception as e:
            messages.error(
                request, "Atributo não adicionado aconteceu algum erro inesperado!"
            )
            return redirect("/admin/atributo_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.change_produtoatributo")
def edit_atributo_produto(request, id):
    atributo = ProdutoAtributo.objects.get(id=id)
    if request.method == "GET":
        return render(request, "produto/atributo/edit.html", {"atributo": atributo})
    elif request.method == "POST":
        try:
            nome = request.POST.get("nome_atributo")
            valor = request.POST.get("valor_atributo")

            atributo.nome = nome
            atributo.valor = valor
            atributo.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoAtributo).id,
                atributo.id,
                f"EDIT -> {atributo.id}",
                CHANGE,
                "O atributo %s foi editado" % atributo.id,
            )

            messages.success(request, "Atributo editado com sucesso!")
            return redirect("/admin/atributo_produto/")
        except Exception as e:
            messages.error(
                request, "Atributo não editado aconteceu algum erro inesperado!"
            )
            return redirect("/admin/atributo_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.delete_produtoatributo")
def delete_atributo_produto(request, id):
    atributo = ProdutoAtributo.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(ProdutoAtributo).id,
            atributo.id,
            f"DELETE -> {atributo.id}",
            DELETION,
            "O atributo %s foi deletado" % atributo.id,
        )

        atributo.delete()

        messages.success(request, "Atributo deletado com sucesso!")
        return redirect("/admin/atributo_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.add_produtoatributo")
def produto_atributo_produto(request, id):
    atributo = ProdutoAtributo.objects.get(id=id)
    produtos = Produto.objects.all().order_by("-id")
    table_relacionada = ProdutoAtributoProduto.objects.filter(atributo_id=id)
    if request.method == "GET":
        products = []
        marcado = False
        for produto in produtos:
            for item in table_relacionada:
                if item.produto_id == produto.id:
                    marcado = True
                    break
                else:
                    marcado = False

            produto = {
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria.nome,
                "tipo": produto.tipo.get_tipo_id_display,
                "data_cad": produto.data_cad,
                "marcado": marcado,
            }
            products.append(produto)

        context = {}
        context["produtos"] = products
        context["table_relacionada"] = table_relacionada
        context["atributo"] = atributo
        return TemplateResponse(
            request, "produto/atributo/produto_atributo.html", context
        )
    elif request.method == "POST":
        try:
            list_id_products = request.POST.getlist("produto_id[]")
            for i in table_relacionada:
                i.delete()
            for i in list_id_products:
                produto = ProdutoAtributoProduto(
                    atributo_id=atributo.id,
                    produto_id=i,
                )
                produto.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoAtributo).id,
                atributo.id,
                f"ADD -> {atributo.nome}",
                ADDITION,
                "Os produtos foram adicionados ao atributo",
            )

            messages.success(request, "Os produtos foram adicionados ao atributo!")
            return redirect("/admin/atributo_produto/")
        except Exception as e:
            messages.error(
                request,
                "Os produtosnão foram adicionados ao atributo, algum erro inesperado!",
            )
            return redirect("/admin/atributo_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.view_produtodiamentro")
def diametro_produto(request):
    if request.method == "GET":
        list_produtos_diametro = ProdutoDiamentro.objects.all().order_by("-id")
        paginator = Paginator(list_produtos_diametro, 10)
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            page = 1
        try:
            list_diameters = paginator.page(page)
        except (EmptyPage, InvalidPage):
            list_diameters = paginator.page(paginator.num_pages)
        return render(
            request, "produto/diametro/index.html", {"list_diameters": list_diameters}
        )


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.add_produtodiamentro")
def create_diametro_produto(request):
    if request.method == "GET":
        form_codigo_servico = FormCodigoServico()
        form_codigo_formato = FormCodigoFormato()
        context = {
            "form_codigo_servico": form_codigo_servico,
            "form_codigo_formato": form_codigo_formato,
        }
        return render(request, "produto/diametro/create.html", context=context)
    elif request.method == "POST":
        nCdServico = request.POST.get("nCdServico")
        sCepOrigem = request.POST.get("sCepOrigem")
        nVlPeso = request.POST.get("nVlPeso")
        nCdFormato = request.POST.get("nCdFormato")
        nVlComprimento = request.POST.get("nVlComprimento")
        nVlAltura = request.POST.get("nVlAltura")
        nVlLargura = request.POST.get("nVlLargura")
        nVlDiametro = request.POST.get("nVlDiametro")

        try:
            produto_diametro = ProdutoDiamentro(
                nCdServico=nCdServico,
                sCepOrigem=sCepOrigem,
                nVlPeso=nVlPeso,
                nCdFormato=nCdFormato,
                nVlComprimento=Decimal(nVlComprimento),
                nVlAltura=Decimal(nVlAltura),
                nVlLargura=Decimal(nVlLargura),
                nVlDiametro=Decimal(nVlDiametro),
            )
            produto_diametro.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoDiamentro).id,
                produto_diametro.id,
                f"ADD -> {produto_diametro.id}",
                ADDITION,
                "O diametro %s foi adicionado" % produto_diametro.id,
            )

            messages.success(request, "Diametro adicionado com sucesso!")
            return redirect("/admin/diametro_produto/")
        except Exception as e:
            messages.error(
                request, "Diametro não adicionado aconteceu algum erro inesperado!"
            )
            return redirect("/admin/create_diametro_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.change_produtodiamentro")
def edit_diametro_produto(request, id):
    diametro_produto = ProdutoDiamentro.objects.get(id=id)
    if request.method == "GET":
        form_codigo_servico = FormCodigoServico()
        form_codigo_formato = FormCodigoFormato()

        context = {
            "diametro_produto": diametro_produto,
            "form_codigo_servico": form_codigo_servico,
            "form_codigo_formato": form_codigo_formato,
        }
        return render(request, "produto/diametro/edit.html", context=context)
    if request.method == "POST":
        nCdServico = request.POST.get("nCdServico")
        sCepOrigem = request.POST.get("sCepOrigem")
        nVlPeso = request.POST.get("nVlPeso")
        nCdFormato = request.POST.get("nCdFormato")
        nVlComprimento = request.POST.get("nVlComprimento")
        nVlAltura = request.POST.get("nVlAltura")
        nVlLargura = request.POST.get("nVlLargura")
        nVlDiametro = request.POST.get("nVlDiametro")

        nVlComprimento = nVlComprimento.replace(",", ".")
        nVlAltura = nVlAltura.replace(",", ".")
        nVlLargura = nVlLargura.replace(",", ".")
        nVlDiametro = nVlDiametro.replace(",", ".")

        try:
            diametro_produto.nCdServico = nCdServico
            diametro_produto.sCepOrigem = sCepOrigem
            diametro_produto.nVlPeso = nVlPeso
            diametro_produto.nCdFormato = nCdFormato
            diametro_produto.nVlComprimento = Decimal(nVlComprimento)
            diametro_produto.nVlAltura = Decimal(nVlAltura)
            diametro_produto.nVlLargura = Decimal(nVlLargura)
            diametro_produto.nVlDiametro = Decimal(nVlDiametro)
            diametro_produto.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoDiamentro).id,
                diametro_produto.id,
                f"EDIT -> {diametro_produto.id}",
                CHANGE,
                "O diametro %s foi editado" % diametro_produto.id,
            )

            messages.success(request, "Diametro editado com sucesso!")
            return redirect("/admin/diametro_produto/")
        except Exception as e:
            messages.error(
                request, "Diametro não editado aconteceu algum erro inesperado!"
            )
            return redirect(f"/admin/edit_diametro_produto/{id}")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.delete_produtodiamentro")
def delete_diametro_produto(request, id):
    diametro = ProdutoDiamentro.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(
            request.user.id,
            ContentType.objects.get_for_model(ProdutoDiamentro).id,
            diametro.id,
            f"DELETE -> {diametro.id}",
            DELETION,
            "O diametro %s foi deletado" % diametro.id,
        )
        diametro.delete()

        messages.success(request, "Diametro deletado com sucesso!")
        return redirect("/admin/diametro_produto/")


@login_required(login_url="/admin")
@manager_required(login_url="/admin")
@permission_required("produto.add_produtodiamentro")
def produto_diametro_produto(request, id):
    diametro = ProdutoDiamentro.objects.get(id=id)
    produtos = Produto.objects.all().order_by("-id")
    table_relacionada = ProdutoDiamentroProduto.objects.filter(diametro_id=id)
    if request.method == "GET":
        products = []
        marcado = False
        for produto in produtos:
            for item in table_relacionada:
                if item.produto_id == produto.id:
                    marcado = True
                    break
                else:
                    marcado = False

            produto = {
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria.nome,
                "tipo": produto.tipo.get_tipo_id_display,
                "data_cad": produto.data_cad,
                "marcado": marcado,
            }
            products.append(produto)

        context = {}
        context["produtos"] = products
        context["table_relacionada"] = table_relacionada
        context["diametro"] = diametro
        return TemplateResponse(
            request, "produto/diametro/produto_diametro.html", context
        )
    elif request.method == "POST":
        try:
            list_id_products = request.POST.getlist("produto_id[]")
            for i in table_relacionada:
                i.delete()
            for i in list_id_products:
                diametro_produto = ProdutoDiamentroProduto(
                    diametro_id=diametro.id,
                    produto_id=i,
                )
                diametro_produto.save()

            LogEntry.objects.log_action(
                request.user.id,
                ContentType.objects.get_for_model(ProdutoDiamentroProduto).id,
                diametro.id,
                f"ADD -> {diametro.id}",
                ADDITION,
                "Os produtos foram adicionados ao diametro",
            )

            messages.success(request, "Os produtos foram adicionados ao diametro!")
            return redirect("/admin/diametro_produto/")
        except Exception as e:
            messages.error(
                request,
                "Os produtos não foram adicionados ao diametro, algum erro inesperado!",
            )
            return redirect(f"/admin/produto_diametro_produto/{id}")
