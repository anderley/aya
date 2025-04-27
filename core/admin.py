from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import(
    Banco, Categoria, CentroCusto, TipoLancamento,
    MotivoExclusao, Indicador
)
from .resources import(
     BancosResource, CategoriasResource,
     CentroCustosResource, TipoLancamentosResource,
     MotivosExclusaoResource, IndicadorResource
)


class BancosAdmin(ImportExportModelAdmin):
    resource_class = BancosResource
    list_display = [
        "id",
        "nome",
        "created_at",
        "updated_at"
    ]
    list_display_links = [
        "nome"
    ]

    class Media:
        css = {
            "all": ["css/custom_admin.css"]
        }


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


class TipoLancamentoAdmin(ImportExportModelAdmin):
    resource_class = TipoLancamentosResource
    list_display = [
        "id",
        "descricao",
        "indicador",
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


class MotivosExclusaoAdmin(ImportExportModelAdmin):
    resource_class = MotivosExclusaoResource
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


class IndicadorAdmin(ImportExportModelAdmin):
    resource_class = IndicadorResource
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


admin.site.register(Banco, BancosAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(CentroCusto, CentroCustoAdmin)
admin.site.register(TipoLancamento, TipoLancamentoAdmin)
admin.site.register(MotivoExclusao, MotivosExclusaoAdmin)
admin.site.register(Indicador, IndicadorAdmin)
