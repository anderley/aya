from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Categoria
from .resources import CategoriasResource


class CategoriaAdmin(ImportExportModelAdmin):
    resource_class = CategoriasResource
    list_display = [
        "id",
        "descricao",
        "tipo_lancamento",
        "created_at",
        "updated_at"
    ]
    list_display_links = [
        "descricao"
    ]

    class Media:
        css = {
            "all": ["css/custom_admin.css"]
        }


admin.site.register(Categoria, CategoriaAdmin)
