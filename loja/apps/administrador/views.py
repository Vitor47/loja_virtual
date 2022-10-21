#Paginator
from tokenize import group
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#Cria Data Automático
from sqlite3 import Date
#Mensagens Template
from django.contrib import messages
#Atenticação de Login e Session
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required, permission_required
#Cripto senhas
from django.contrib.auth.hashers import make_password
#Retornar templates
from django.shortcuts import redirect, render
#Importa demais coisas
from django.contrib.auth.models import User, Permission, Group
from slug import slug
#Cria LOG dos registros
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
#Permissões

from .models import Banner, Configuracao, Produto, ProdutoAtributo, ProdutoCategoria, ProdutoImagens, ProdutoTipo, Cliente, Auditoria

def login(request):
    if request.method == "GET":
        return render(request, "login/index.html")
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            if user.is_staff == True or user.is_superuser == True and user.is_active == True:
                login_django(request, user)

                LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                    user.id, f"LOG -> {user.id}", CHANGE, 'O Usuário %s logou no sistema' %user.id
                )

                ip = request.META.get('REMOTE_ADDR')
                request.session['ip'] = ip

                auditoria = Auditoria (
                    user = user,
                    mensagem = "LOGOU NO SISTEMA",
                    ip = f"CLIENTE IP -> {ip}",
                )
                auditoria.save()

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

                    user_verifica = User.objects.exclude(id__gte=user.id).filter(username__gte=username)
                    for item in user_verifica:
                        if item.username == username:
                            messages.error(request, "Este usuário já existe por favor digite um usuário diferente!")
                            return redirect('/admin/perfil/')

                    email_verifica = User.objects.exclude(id__gte=user.id).filter(email__gte=email)
                    for item in email_verifica:
                        if item.email == email:
                            messages.error(request, "Este E-mail já existe por favor digite um e-mail diferente!")
                            return redirect('/admin/perfil/')

                    user.first_name = nome
                    user.username = username
                    user.email = email
                    user.save()

                    LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                        user.id, f"EDIT -> {user.first_name + '-' + user.username + '-' + user.email}", CHANGE, 'O Usuário com id -> %s alterou o perfil' %user.id
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
@permission_required('administrador.add_banner', login_url="/admin/banner/")
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
        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Banner).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'O banner %s foi deletado' %item.id
        )

        item.delete()
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

        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Configuracao).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'A configuração %s foi deletada' %item.id
        )

        item.delete()
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
    elif request.method == "POST":
        try:
            nome = request.POST.get('nome_user')
            sobrenome = request.POST.get('sobrenome_user')
            username = request.POST.get('username_user')
            email = request.POST.get('email_user')
            senha = request.POST.get('senha_user')
            confirmar_senha_user = request.POST.get('confirmar_senha_user')
            super_admin = request.POST.get('super_admin')
            membro_equipe = request.POST.get('membro_equipe')

            try:
                usuario_username = User.objects.get(username=username)
                usuario_email = User.objects.get(email=email)

                if usuario_email or usuario_username:
                    messages.error(request, "Erro! Já existe um usuário com o mesmo e-mail ou mesmo username!")
                    return redirect('/admin/create_user/')

            except User.DoesNotExist:
                if senha != confirmar_senha_user:
                    return redirect('/admin/create_user/')
                else:
                    if super_admin != None:
                        super_admin = True
                        membro_equipe = True
                    else:
                        super_admin = False
                        membro_equipe = False

                    if membro_equipe != None:
                        membro_equipe = True
                        super_admin = False
                    else:
                        membro_equipe = False
                        super_admin = False

                
                user = User (
                    first_name = nome, 
                    last_name = sobrenome,
                    username = username,
                    email = email,
                    password = make_password(senha),
                    is_active = True,
                    is_staff = membro_equipe,
                    is_superuser = super_admin,
                )

                user.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                user.id, f"ADD -> {user.username + '-' + user.email}", ADDITION, 'O usuário %s foi adicionado' %user.id
            )

            messages.success(request, "Usuário criado com sucesso!")
            return redirect('/admin/usuario/')
        except Exception as e:
            messages.error(request, "Usuário não criado algum erro inesperado!")
            return redirect(f'/admin/create_user/')

@login_required(login_url="/admin")
def edit_user(request, id):
    user = User.objects.get(id=id)
    if request.method == "GET":
        if user.username == "vitor.miolo" or user.email == "vitormateusmiolo@gmail.com":
            messages.error(request, "Você não tem acesso para editar esse usuário!")
            return redirect('/admin/usuario/')

        return render(request, "usuarios/edit.html", {'user': user})
    elif request.method == "POST":
        try:
            nome = request.POST.get('nome_user')
            sobrenome = request.POST.get('sobrenome_user')
            username = request.POST.get('username_user')
            email = request.POST.get('email_user')
            senha = request.POST.get('senha_user')
            confirmar_senha_user = request.POST.get('confirmar_senha_user')
            super_admin = request.POST.get('super_admin')
            membro_equipe = request.POST.get('membro_equipe')
            status = request.POST.get('status')

            if status == "1":
                status = True
            elif status == "2":
                status = False

            try:
                usuario_username = User.objects.exclude(id__gte=user.id).get(username=username)
                usuario_email = User.objects.exclude(id__gte=user.id).get(email=email)

                if usuario_email or usuario_username:
                    messages.error(request, "Erro! Já existe um usuário com o mesmo e-mail ou mesmo usuário!")
                    return redirect('/admin/edit_user/{id}')

            except User.DoesNotExist:
                if senha != confirmar_senha_user:
                    return redirect('/admin/edit_user/{id}')
                else:
                    if super_admin != None:
                        super_admin = True
                        membro_equipe = True
                    else:
                        super_admin = False
                        membro_equipe = False

                    if membro_equipe != None:
                        membro_equipe = True
                        super_admin = False
                    else:
                        membro_equipe = False
                        super_admin = False

                    user.first_name = nome
                    user.last_name = sobrenome
                    user.username = username
                    user.email = email
                    user.set_password(senha)
                    user.is_active = status
                    user.is_staff = membro_equipe
                    user.is_superuser = super_admin

                    user.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
                user.id, f"EDITOU -> {user.username + '-' + user.email}", CHANGE, 'O usuário %s foi editado' %user.id
            )

            messages.success(request, "Usuário editado com sucesso!")
            return redirect('/admin/usuario/')
        except Exception as e:
            messages.error(request, "Usuário não editado algum erro inesperado!")
            return redirect(f'/admin/edit_user/{id}')

@login_required(login_url="/admin")
def delete_user(request, id):
    item = User.objects.get(id=id)
    if request.method == "GET":
        if item.username == "vitor.miolo" or item.email == "vitormateusmiolo@gmail.com":
            messages.error(request, "Você não tem acesso para deletar esse usuário!")
            return redirect('/admin/usuario/')

        LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(User).id,
            item.id, f"DELETE -> {item.id}", DELETION, 'O usuário %s foi deletado' %item.id
        )

        item.delete()

        messages.success(request, "Usuário deletado com sucesso!")
        return redirect('/admin/usuario/')

@login_required(login_url="/admin")
def grupo_acesso(request):
    if request.method == "GET":
        groups = Group.objects.all()
        return render(request, "grupo_acesso/index.html", {'groups': groups})

@login_required(login_url="/admin")
def create_grupo_acesso(request):
    if request.method == "GET":
        return render(request, "grupo_acesso/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get('nome_group')
            try:
                name = Group.objects.get(name=nome)
                if name:
                    messages.error(request, "Erro! Já existe um grupo com o mesmo nome!")
                    return redirect('/admin/create_grupo_acesso/')

            except Group.DoesNotExist:
                group = Group (
                    name = nome, 
                )
                group.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Group).id,
                group.id, f"ADD -> {group.name}", ADDITION, 'O grupo %s foi adicionado' %group.id
            )

            messages.success(request, "Grupo criado com sucesso!")
            return redirect('/admin/grupo_acesso/')
        except Exception as e:
            print(e)
            messages.error(request, "Grupo não criado algum erro inesperado!")
            return redirect(f'/admin/grupo_acesso/')

@login_required(login_url="/admin")
def add_users_group(request, id_group):
    users = User.objects.exclude(is_superuser__gte=True).all()
    grupo = User.objects.get(id=id_group)
    if request.method == "GET":
        return render(request, "grupo_acesso/users.html", {'users': users, 'grupo': grupo})
    elif request.method == "POST":
        try:
            list_id_users = request.POST.getlist('user_id[]')
            for _id in list_id_users:
                id = int(_id)
                user = User.objects.get(id=id)
                group = Group.objects.get(id=id_group)
                user.groups.add(group)

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Group).id,
                grupo.id, f"ADD ->", ADDITION, 'Os Usuários %s foram adicionados ao grupo' %grupo.id
            )

            messages.success(request, "Usuários foram adicionados ao grupo com sucesso!")
            return redirect('/admin/grupo_acesso/')
        except Exception as e:
            messages.error(request, "Usuários não foram adicionados ao grupo algum erro inesperado!")
            return redirect('/admin/grupo_acesso/')

@login_required(login_url="/admin")
def add_permission_group(request):
    if request.method == "GET":
        return render(request, "grupo_acesso/create.html")
    elif request.method == "POST":
        try:
            nome = request.POST.get('nome_group')
            try:
                name = Group.objects.get(name=nome)
                if name:
                    messages.error(request, "Erro! Já existe um grupo com o mesmo nome!")
                    return redirect('/admin/create_grupo_acesso/')

            except Group.DoesNotExist:
                group = Group (
                    name = nome, 
                )
                group.save()

            LogEntry.objects.log_action(request.user.id, ContentType.objects.get_for_model(Group).id,
                group.id, f"ADD -> {group.name}", ADDITION, 'O grupo %s foi adicionado' %group.id
            )

            messages.success(request, "Grupo criado com sucesso!")
            return redirect('/admin/grupo_acesso/')
        except Exception as e:
            print(e)
            messages.error(request, "Grupo não criado algum erro inesperado!")
            return redirect(f'/admin/grupo_acesso/')