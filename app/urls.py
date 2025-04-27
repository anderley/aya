from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auditoria/', include('audit.urls')),
    path('admin/', admin.site.urls),
    path('', include('main.urls'), name='home'),
    path('contas_pagar/', include('contas_pagar.urls')),
    path('contas_receber/', include('contas_receber.urls')),
    path('empresas/', include('empresas.urls')),
    path('estoques/', include('estoques.urls')),
    path('dre/', include('dre.urls')),
    path('fornecedores/', include('fornecedores.urls')),
    path('usuarios/', include('usuarios.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
