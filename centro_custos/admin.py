from django.contrib import admin

from .models import CentroCusto


class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ["descricao"]


admin.site.register(CentroCusto, CentroCustoAdmin)
