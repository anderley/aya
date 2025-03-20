from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import MotivoExclusao
from .resources import MotivosExclusaoResource


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


admin.site.register(MotivoExclusao, MotivosExclusaoAdmin)
