from django.urls import path

from .views import (EstoqueCreateView, EstoqueDeleteView,
                    EstoqueListView, EstoqueUpdateView,
                    delete_items)

urlpatterns = [
    path('', EstoqueListView.as_view(), name='listar_estoques'),
    path(
        'add/', EstoqueCreateView.as_view(),
        name='incluir_estoque'
    ),
    path(
        'edit/<int:pk>', EstoqueUpdateView.as_view(),
        name='editar_estoque'
    ),
    path(
        'delete/<int:pk>', EstoqueDeleteView.as_view(),
        name='deletar_estoque'
    ),
    path('delete-items', delete_items, name='deletar_items_estoque'),
]
