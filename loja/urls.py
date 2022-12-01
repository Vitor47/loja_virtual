from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('admin/', include('loja.apps.apps_administrador.banner.urls', namespace='loja.apps.apps_administrador.banner')),
    path('admin/', include('loja.apps.apps_administrador.cliente.urls', namespace='loja.apps.apps_administrador.cliente')),
    path('admin/', include('loja.apps.apps_administrador.configuracao.urls', namespace='loja.apps.apps_administrador.configuracao')),
    path('admin/', include('loja.apps.apps_administrador.dashboard.urls', namespace='loja.apps.apps_administrador.dashboard')),
    path('admin/', include('loja.apps.apps_administrador.produto.urls', namespace='loja.apps.apps_administrador.produto')),
    path('admin/', include('loja.apps.apps_administrador.sistema.urls', namespace='loja.apps.apps_administrador.sistema')),
    path('', include('loja.apps.site_loja.urls', namespace='loja.apps.site_loja')),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
