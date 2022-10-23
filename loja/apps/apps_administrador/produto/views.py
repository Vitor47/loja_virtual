#Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#Cria Data Automático
from sqlite3 import Date
#Mensagens Template
from django.contrib import messages
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required
#Retornar templates
from django.shortcuts import redirect, render
#Importa demais coisas
from django.contrib.auth.models import User, Permission, Group
from slug import slug
#Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
#Permissões

from .models import Produto, ProdutoAtributo, ProdutoCategoria, ProdutoImagens, ProdutoTipo

@login_required(login_url="/admin")
def produto(request):
    list_products = Produto.objects.all()
    paginator = Paginator(list_products, 3) # Mostra 25 contatos por página

    # Make sure page request is an int. If not, deliver first page.
    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "produto/index.html", {'produtos': products})

@login_required(login_url="/admin")
def search_produto(request):
    list_products = Produto.objects.all()
    #usuarios = User.objects.all()
    consulta_nome = request.GET.get('pesquisar_por_nome')
    #q = request.GET.get('pesquisar_por')

    # Buscar por usuário
    if consulta_nome is not None:
        list_products = list_products.filter(nome__icontains=consulta_nome)
    paginator = Paginator(list_products, 3) # Mostra 25 contatos por página

    # Make sure page request is an int. If not, deliver first page.
    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request, "produto/index.html", {'produtos': products})

@login_required(login_url="/admin")
def create_produto(request):
    if request.method == "GET":
        list_tipos = ProdutoTipo.objects.all()
        list_categoria = ProdutoCategoria.objects.all()
        list_atributos = ProdutoAtributo.objects.all()
        return render(request, "produto/create.html", {'tipos': list_tipos, 'categorias': list_categoria, 'atributos': list_atributos})
    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            nome = request.POST.get('nome_produto')
            valor = request.POST.get('valor_produto')
            quantidade = request.POST.get('quantidade_produto')
            image = request.FILES.get('image_produto')
            descricao = request.POST.get('descricao_produto')
            desconto = request.POST.get('desconto_produto')
            tipo = request.POST.get('tipo_produto')
            categoria = request.POST.get('categoria_produto')
            atributo = request.POST.get('atributo_produto')

            valor_formatado = valor.replace("R$:","").replace(".", "").replace(",", ".")
            valor_formatado_desconto = desconto.replace("R$:","").replace(".", "").replace(",", ".")

            produto = Produto (
                nome = nome,
                slug = slug(nome),             
                valor = valor_formatado,
                quantidade = int(quantidade),
                imagem_principal = image,
                desconto = valor_formatado_desconto,
                status = True,
                categoria_id = int(categoria),
                atributo_id = int(atributo),
                tipo_id = int(tipo),
                descricao = descricao,
                user_cad = user,
                data_cad = Date.today(),
            )
            produto.save()

            produto.slug = slug(produto.nome) + "_" + str(produto.id)
            produto.save()

            list_imagens = request.FILES.getlist('imagens_produto[]', None)
            for i in range(len(list_imagens)):
                if list_imagens[i] != None:
                    produto_imagem = ProdutoImagens (
                        imagem = list_imagens[i],
                        produto_id = produto.id,
                        user_cad = user,
                        data_cad = Date.today(),
                    )
                    produto_imagem.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Produto).id,
                produto.id, f"ADD -> {produto.id}", ADDITION, 'O produto %s foi adicionado' %produto.id
            )

            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect(f'/admin/produto/')
        except Exception as e:
            print(e)
            messages.error(request, "Produto não cadastrado algum erro inesperado!")
            return redirect(f'/admin/create_produto/')

@login_required(login_url="/admin")
def edit_produto(request, id):
    item = Produto.objects.get(id=id)
    list_tipos = ProdutoTipo.objects.all()
    list_categoria = ProdutoCategoria.objects.all()
    list_atributos = ProdutoAtributo.objects.all()
    list_imagens = ProdutoImagens.objects.filter(produto_id=id)
    if request.method == 'GET':
        return render(request, "produto/edit.html", {'produto': item, 'tipos': list_tipos, 'categorias': list_categoria, 'atributos': list_atributos, 'imagens': list_imagens})
    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            nome = request.POST.get('nome_produto')
            status = request.POST.get('status')
            valor = request.POST.get('valor_produto')
            quantidade = request.POST.get('quantidade_produto')
            image = request.FILES.get('image_produto')
            descricao = request.POST.get('descricao_produto')
            desconto = request.POST.get('desconto_produto')
            tipo = request.POST.get('tipo_produto')
            categoria = request.POST.get('categoria_produto')
            atributo = request.POST.get('atributo_produto')

            valor_formatado = valor.replace("R$:","").replace(".", "").replace(",", ".")
            valor_formatado_desconto = desconto.replace("R$:","").replace(".", "").replace(",", ".")

            if image == None:
                item.imagem_principal = item.imagem_principal
            else:
                item.imagem_principal = image

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
            item.atributo_id = int(atributo)
            item.descricao = descricao
            item.data_cad = item.data_cad
            item.user_cad = item.user_cad
            item.dat_edit = Date.today()
            item.save()

            list_imagens = request.FILES.getlist('imagens_produto[]', None)
            for i in range(len(list_imagens)):
                if list_imagens[i] != None:
                    produto_imagem = ProdutoImagens (
                        imagem = list_imagens[i],
                        produto_id = item.id,
                        user_cad = user,
                        data_cad = Date.today(),
                    )
                    produto_imagem.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Produto).id,
                item.id, f"EDIT -> {item.id}", CHANGE, 'O produto %s foi editado' %item.id
            )

            messages.success(request, "Produto editado com sucesso!")
            return redirect(f'/admin/produto/')
        except Exception as e:
            print(e)
            messages.error(request, "Produto não editado algum erro inesperado!")
            return redirect(f'/admin/edit_produto/{id}')

@login_required(login_url="/admin")
def delete_produto(request, id):
    item = Produto.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Produto).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'O produto %s foi deletado' %item.id
        )

        item.delete()     
        messages.success(request, "Produto deletado com sucesso!")
        return redirect(f'/admin/produto/')

@login_required(login_url="/admin")
def delete_image_produto(request, id):
    item = ProdutoImagens.objects.get(id=id)
    if request.method == "GET":
        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(ProdutoImagens).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'A imagem do produto %s foi deletado' %item.id
        )

        item.delete()

        messages.success(request, "Imagem deletada com sucesso!")
        return redirect(f'/admin/edit_produto/{item.produto_id}')