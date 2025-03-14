from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .resources import CentroCustosResource
from .models import CentroCusto


class CentroCustoAdmin(ImportExportModelAdmin):
    resource_class = CentroCustosResource
    list_display = [
        "id",
        "descricao",
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


admin.site.register(CentroCusto, CentroCustoAdmin)
