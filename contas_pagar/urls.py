from django.urls import path

from .views import (ContasPagarCreateView, ContasPagarDeleteView,
                    ContasPagarListView, ContasPagarUpdateView, delete_items)

urlpatterns = [
    path('', ContasPagarListView.as_view(), name='listar_contas_pagar'),
    path('add/', ContasPagarCreateView.as_view(), name='incluir_conta_pagar'),
    path(
        'edit/<int:pk>', ContasPagarUpdateView.as_view(),
        name='editar_conta_pagar'
    ),
    path(
        'delete/<int:pk>', ContasPagarDeleteView.as_view(),
        name='deletar_conta_pagar'
    ),
    path('delete-items', delete_items, name='deletar_items_conta_pagar'),
]
