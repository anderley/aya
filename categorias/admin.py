from django.contrib import admin

from .models import Categoria


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["descricao", "tipo_lancamento"]


admin.site.register(Categoria, CategoriaAdmin)
