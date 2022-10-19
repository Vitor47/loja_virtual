from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path('admin/', include('loja.apps.administrador.urls', namespace='loja.apps.administrador')),
    path('', include('loja.apps.site_loja.urls', namespace='loja.apps.site_loja')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
