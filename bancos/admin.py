from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .resources import BancosResource
from .models import Banco


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


admin.site.register(Banco, BancosAdmin)
