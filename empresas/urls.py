from django.urls import path

from .views import EmpresasListView, EmpresasCreateView, EmpresasUpdateView, EmpresasDeleteView

urlpatterns = [
    path('', EmpresasListView.as_view(), name='listar_empresas'),
    path('add/', EmpresasCreateView.as_view(), name='incluir_empresa'),
    path('edit/<int:pk>', EmpresasUpdateView.as_view(), name='editar_empresa'),
    path('delete/<int:pk>', EmpresasDeleteView.as_view(), name='deletar_empresa'),
]