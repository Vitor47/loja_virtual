from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path(
        "admin/",
        include(
            "apps.admin.banner.urls",
            namespace="apps.admin.banner",
        ),
    ),
    path(
        "admin/",
        include(
            "apps.admin.cliente.urls",
            namespace="apps.admin.cliente",
        ),
    ),
    path(
        "admin/",
        include(
            "apps.admin.configuracao.urls",
            namespace="apps.admin.configuracao",
        ),
    ),
    path(
        "admin/",
        include(
            "apps.admin.dashboard.urls",
            namespace="apps.admin.dashboard",
        ),
    ),
    path(
        "admin/",
        include(
            "apps.admin.produto.urls",
            namespace="apps.admin.produto",
        ),
    ),
    path(
        "admin/",
        include(
            "apps.admin.sistema.urls",
            namespace="apps.admin.sistema",
        ),
    ),
    path("", include("apps.site.urls", namespace="loja.apps.site")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
