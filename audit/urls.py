from django.urls import path

from .views import AuditoriasListView

urlpatterns = [
    path('', AuditoriasListView.as_view(), name='listar_auditorias'),
]
