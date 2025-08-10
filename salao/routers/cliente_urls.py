from django.urls import path
from ..views.cliente_view import cliente_create,cliente_edit,clientes_list

app_name = 'clientes'

urlpatterns = [
    path('', clientes_list, name='clientes_list'),
    path('novo/', cliente_create, name='cliente_create'),
    path('<int:pk>/editar/', cliente_edit, name='cliente_edit'),
]