from django.urls import path
from . import views

app_name = 'apps_administrador.produto'

urlpatterns = [
    path('produto/', views.produto, name='produto'),
    path('search_produto/', views.search_produto, name='search_produto'),
    path('create_produto/', views.create_produto, name='create_produto'),
    path('edit_produto/<int:id>', views.edit_produto, name='edit_produto'),
    path('delete_produto/<int:id>', views.delete_produto, name='delete_produto'),
    path('delete_image_produto/<int:id>', views.delete_image_produto, name='delete_image_produto'),
    ]
