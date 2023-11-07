from django.urls import path
from .views import pagamento

app_name = "admin.pagamento"

urlpatterns = [
    path("pagamento/", pagamento, name="pagamento"),
]
