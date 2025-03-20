from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import TipoLancamento
from .resources import TipoLancamentosResource


class TipoLancamentoAdmin(ImportExportModelAdmin):
    resource_class = TipoLancamentosResource
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


admin.site.register(TipoLancamento, TipoLancamentoAdmin)
