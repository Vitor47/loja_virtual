from django.urls import path
from . import views

app_name = 'administrador'

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('senha/', views.senha, name='senha'),
    path('sair/', views.sair, name='sair'),
    path('banner/', views.banner, name='banner'),
    path('create_banner/', views.create_banner, name='create_banner'),
    path('edit_banner/<int:id>', views.edit_banner, name='edit_banner'),
    path('delete_banner/<int:id>', views.delete_banner, name='delete_banner'),
    path('produto/', views.produto, name='produto'),
    path('search_produto/', views.search_produto, name='search_produto'),
    path('create_produto/', views.create_produto, name='create_produto'),
    path('edit_produto/<int:id>', views.edit_produto, name='edit_produto'),
    path('delete_produto/<int:id>', views.delete_produto, name='delete_produto'),
    path('delete_image_produto/<int:id>', views.delete_image_produto, name='delete_image_produto'),
    path('configuracao/', views.configuracao, name='configuracao'),
    path('create_configuracao/', views.create_configuracao, name='create_configuracao'),
    path('edit_configuracao/<int:id>', views.edit_configuracao, name='edit_configuracao'),
    path('delete_configuracao/<int:id>', views.delete_configuracao, name='delete_configuracao'),
    path('cliente/', views.cliente, name='cliente'),
    path('search_cliente/', views.search_cliente, name='search_cliente'),
    path('usuario/', views.list_user, name='list_user'),
    path('create_user/', views.create_user, name='create_user'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('grupo_acesso/', views.grupo_acesso, name='grupo_acesso'),
    path('create_grupo_acesso/', views.create_grupo_acesso, name='create_grupo_acesso'),
    path('add_users_group/<int:id_group>', views.add_users_group, name='add_users_group'),
    path('add_permission_group/', views.add_permission_group, name='add_permission_group'),
    ]
