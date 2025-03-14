from django.urls import path

from .views import FornecedoresListView, FornecedoresCreateView, FornecedoresUpdateView, FornecedoresDeleteView

urlpatterns = [
    path('', FornecedoresListView.as_view(), name='listar_fornecedores'),
    path('add/', FornecedoresCreateView.as_view(), name='incluir_fornecedor'),
    path('edit/<int:pk>', FornecedoresUpdateView.as_view(), name='editar_fornecedor'),
    path(
        'delete/<int:pk>',
        FornecedoresDeleteView.as_view(),
        name='deletar_fornecedor'
    ),
]
