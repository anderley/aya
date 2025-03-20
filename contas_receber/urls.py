from django.urls import path

from .views import (ContasReceberCreateView, ContasReceberDeleteView,
                    ContasReceberListView, ContasReceberUpdateView,
                    delete_items)

urlpatterns = [
    path('', ContasReceberListView.as_view(), name='listar_contas_receber'),
    path(
        'add/', ContasReceberCreateView.as_view(),
        name='incluir_conta_receber'
    ),
    path(
        'edit/<int:pk>', ContasReceberUpdateView.as_view(),
        name='editar_conta_receber'
    ),
    path(
        'delete/<int:pk>', ContasReceberDeleteView.as_view(),
        name='deletar_conta_receber'
    ),
    path('delete-items', delete_items, name='deletar_items_conta_receber'),
]
