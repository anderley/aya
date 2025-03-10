from django.contrib import admin

from .models import TipoLancamento


class TipoLancamentoAdmin(admin.ModelAdmin):
    list_display = ["descricao"]


admin.site.register(TipoLancamento, TipoLancamentoAdmin)
