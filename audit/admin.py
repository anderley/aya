from django.contrib import admin

from .models import Auditoria


class AuditoriaAdmin(admin.ModelAdmin):
    actions = ()
    list_display = ["acao", "motivo", "registro", "created_at", "updated_at"]


admin.site.register(Auditoria, AuditoriaAdmin)
