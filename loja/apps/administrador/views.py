#Paginator
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#Cria Data Automático
from sqlite3 import Date
#Mensagens Template
from django.contrib import messages
#Atenticação de Login e Session
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
#Retornar templates
from django.shortcuts import redirect, render
#Importa demais coisas
from django.contrib.auth.models import User
from slug import slug
#Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

from .models import Banner, Configuracao, Produto, ProdutoAtributo, ProdutoCategoria, ProdutoImagens, ProdutoTipo, Cliente

def login(request):
    if request.method == "GET":
        return render(request, "login/index.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            if user.is_staff == True and user.is_superuser == True and user.is_active == True:
                login_django(request, user)

                LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                    user.id, f"LOG -> {user.id}", CHANGE, 'O Usuário %s logou no sistema' %user.id
                )
                return redirect('/admin/dashboard/')
            else:
                messages.error(request, "Usuário não tem permissão!")
                return redirect('/admin') 
        else:
            messages.error(request, "Usuário ou senha incorretos!")
            return redirect('/admin')

@login_required(login_url="/admin")
def perfil(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            return render(request, "perfil/index.html", {'usuario': user})
        elif request.method == "POST":
            try:
                if user:
                    nome = request.POST.get('nome_usuario')
                    username = request.POST.get('usuario')
                    email = request.POST.get('email_usuario')

                    user.first_name = nome
                    user.username = username
                    user.email = email
                    user.save()

                    LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                        user.id, f"EDIT -> {user.id}", CHANGE, 'O Usuário %s alterou o perfil' %user.id
                    )

                    messages.success(request, "Perfil editado com sucesso!")
                    return redirect('/admin/dashboard/')
                else:
                    messages.error(request, "Perfil não encontrado!")
                    return redirect('/admin/perfil/')

            except Exception as e:
                messages.error(request, "Perfil não editado algum erro inesperado!")
                return redirect('/admin/perfil/')
    else:
        return redirect('/admin')

@login_required(login_url="/admin")
def senha(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        if request.method == "GET":
            return render(request, "perfil/senha.html", {'usuario': user})
        elif request.method == "POST":
            try:
                if user:
                    senha_atual = request.POST.get('senha_atual_usuario')
                    senha_nova = request.POST.get('nova_senha_usuario')
                    senha_nova_confirma = request.POST.get('confirmar_nova_senha_usuario')
                    
                    if user.check_password(senha_atual):
                        if senha_nova == senha_nova_confirma:
                            user.set_password(senha_nova_confirma)
                            user.save()

                            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                                user.id, f"EDIT -> {user.id}", CHANGE, 'O Usuário %s alterou a senha' %user.id
                            )

                            messages.success(request, "Senha editada com sucesso!")
                            return redirect('/admin/dashboard/')
                        else:
                            messages.error(request, "A nova senha digitada não confere com a senha digitada para confirmar!")
                            return redirect('/admin/senha/')
                    else:
                        messages.error(request, "Senha atual não confirma com o que foi digitado!")
                        return redirect('/admin/senha/')
                else:
                    messages.error(request, "Perfil não encontrado!")
                    return redirect('/admin/dashboard/')

            except Exception as e:
                messages.error(request, "Senha não editada algum erro inesperado!")
                return redirect('/admin/senha/')
    else:
        return redirect('/admin')

@login_required(login_url="/admin")
def sair(request):
    logout(request)
    return redirect('/admin')

@login_required(login_url="/admin")
def dashboard(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        return render(request, "dashboard/index.html", {'usuario': user})
    else:
        return redirect('/admin')

@login_required(login_url="/admin")
def banner(request):
    banner = Banner.objects.all()
    return render(request, "banner/index.html", {'banner': banner})

@login_required(login_url="/admin")
def create_banner(request):
    if request.method == "GET":
        return render(request, "banner/create.html")
    elif request.method == "POST":
        try:
            user = User.objects.get(id=request.user.id)
            image = request.FILES.get('image_banner')

            banner = Banner (
                imagem = image,
                status = True,
                user_cad = user,
                data_cad = Date.today()
            )
            banner.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Banner).id,
                banner.id, f"ADD -> {banner.id}", ADDITION, 'O banner %s foi cadastrado' %banner.id
            )

            messages.success(request, "Banner cadastrado com sucesso!")
            return redirect('/admin/banner/')
        except Exception as e:
            messages.error(request, "Banner não cadastrado algum erro inesperado!")
            return redirect('/admin/create_banner/')

@login_required(login_url="/admin")
def edit_banner(request, id):
    item = Banner.objects.get(id=id)
    if request.method == 'GET':
        return render(request, "banner/edit.html", {'banner': item})
    elif request.method == "POST":
        try:
            image = request.FILES.get('image_stand')
            status = request.POST.get('status')

            if image == None:
                item.imagem = item.imagem
            else:
                item.imagem = image

            if status == "1":
                item.status = True
            elif status == "2":
                item.status = False

            item.data_cad = item.data_cad
            item.dat_edit = Date.today()
            item.user_cad = item.user_cad,
            item.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Banner).id,
                item.id, f"EDIT -> {item.id}", CHANGE, 'O banner %s foi editado' %item.id
            )

            messages.success(request, "Banner editado com sucesso!")
            return redirect('/admin/banner/')
        except Exception as e:
            messages.error(request, "Banner não editado algum erro inesperado!")
            return redirect(f'/admin/edit_banner/{id}')

@login_required(login_url="/admin")
def delete_banner(request, id):
    item = Banner.objects.get(id=id)
    if request.method == "GET":
        item.delete()

        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Banner).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'O banner %s foi deletado' %item.id
        )
        messages.success(request, "Banner deletado com sucesso!")
        return redirect('/admin/banner/')

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
        item.delete()

        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Produto).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'O produto %s foi deletado' %item.id
        )
        messages.success(request, "Produto deletado com sucesso!")
        return redirect(f'/admin/produto/')

@login_required(login_url="/admin")
def delete_image_produto(request, id):
    item = ProdutoImagens.objects.get(id=id)
    if request.method == "GET":
        item.delete()

        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(ProdutoImagens).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'A imagem do produto %s foi deletado' %item.id
        )

        messages.success(request, "Imagem deletada com sucesso!")
        return redirect(f'/admin/edit_produto/{item.produto_id}')

@login_required(login_url="/admin")
def configuracao(request):
    if request.method == "GET":
        list_configs = Configuracao.objects.all()
        return render(request, "configuracao/index.html", {'configuracao': list_configs})

@login_required(login_url="/admin")
def create_configuracao(request):
    if request.method == "GET":
        return render(request, "configuracao/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get('nome_configuracao')
            valor = request.POST.get('valor_configuracao')

            configuracao = Configuracao (
                nome = nome,
                valor = valor,
            )
            configuracao.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Configuracao).id,
                configuracao.id, f"ADD -> {configuracao.id}", ADDITION, 'A configuração %s foi adicionada' %configuracao.id
            )

            messages.success(request, "Configuração cadastrada com sucesso!")
            return redirect('/admin/configuracao/')
        except Exception as e:
            messages.error(request, "Configuração não cadastrada algum erro inesperado!")
            return redirect('/admin/create_configuracao/')

@login_required(login_url="/admin")
def edit_configuracao(request, id):
    item = Configuracao.objects.get(id=id)
    if request.method == 'GET':
        return render(request, "configuracao/edit.html", {'configuracao': item})
    elif request.method == "POST":
        try:
            nome = request.POST.get('nome_configuracao')
            valor = request.POST.get('valor_configuracao')

            item.nome = nome 
            item.valor = valor
            item.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Configuracao).id,
                item.id, f"EDIT -> {item.id}", CHANGE, 'A configuração %s foi editada' %item.id
            )

            messages.success(request, "Configuração editada com sucesso!")
            return redirect('/admin/configuracao/')
        except Exception as e:
            messages.error(request, "Configuração não editada algum erro inesperado!")
            return redirect(f'/admin/edit_configuracao/{id}')

@login_required(login_url="/admin")
def delete_configuracao(request, id):
    item = Configuracao.objects.get(id=id)
    if request.method == "GET":
        item.delete()

        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Configuracao).id,
            item.id, f"DELETE -> {item.id}", CHANGE, 'A configuração %s foi deletada' %item.id
        )

        messages.success(request, "Configuração deletada com sucesso!")
        return redirect('/admin/configuracao/')

@login_required(login_url="/admin")
def cliente(request):
    list_clientes = Cliente.objects.all()
    paginator = Paginator(list_clientes, 10) # Mostra 25 contatos por página

    # Make sure page request is an int. If not, deliver first page.
    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        clientes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        clientes = paginator.page(paginator.num_pages)
    return render(request, "clientes/index.html", {'clientes': clientes})

@login_required(login_url="/admin")
def search_cliente(request):
    list_clientes = Cliente.objects.all()
    #usuarios = User.objects.all()
    consulta_nome = request.GET.get('pesquisar_por_nome')
    #q = request.GET.get('pesquisar_por')

    # Buscar por usuário
    if consulta_nome is not None:
        list_clientes = list_clientes.filter(nome__icontains=consulta_nome)
    paginator = Paginator(list_clientes, 10) # Mostra 25 contatos por página

    # Make sure page request is an int. If not, deliver first page.
    # Esteja certo de que o `page request` é um inteiro. Se não, mostre a primeira página.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # Se o page request (9999) está fora da lista, mostre a última página.
    try:
        clientes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        clientes = paginator.page(paginator.num_pages)
    return render(request, "produto/index.html", {'clientes': clientes})

@login_required(login_url="/admin")
def list_user(request):
    if request.method == "GET":
        list_users = User.objects.all()
        return render(request, "usuarios/index.html", {'users': list_users})

@login_required(login_url="/admin")
def create_user(request):
    if request.method == "GET":
        return render(request, "usuarios/create.html")

@login_required(login_url="/admin")
def edit_user(request):
    pass

@login_required(login_url="/admin")
def delete_user():
    pass