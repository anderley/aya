from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


from .models import(
    Banco, Categoria, CentroCusto, TipoLancamento,
    MotivoExclusao, Indicador
)


class BancosResource(resources.ModelResource):

    class Meta:
        model = Banco
        import_id_fields = ["nome"]
        fields = ["id", "nome"]


class CategoriasResource(resources.ModelResource):
    tipo_lancamento = fields.Field(
        column_name="tipo_lancamento",
        attribute="tipo_lancamento",
        widget=ForeignKeyWidget(TipoLancamento, field="descricao")
    )

    class Meta:
        model = Categoria
        import_id_fields = ["descricao"]
        fields = ["id", "descricao", "tipo_lancamento"]


class CentroCustosResource(resources.ModelResource):

    class Meta:
        model = CentroCusto
        import_id_fields = ["descricao"]
        fields = ["id", "descricao"]


class TipoLancamentosResource(resources.ModelResource):
    indicador = fields.Field(
        column_name="indicador",
        attribute="indicador",
        widget=ForeignKeyWidget(Indicador, field="descricao")
    )

    class Meta:
        model = TipoLancamento
        import_id_fields = ["descricao"]
        fields = ["id", "descricao", "indicador"]


class MotivosExclusaoResource(resources.ModelResource):

    class Meta:
        model = MotivoExclusao
        import_id_fields = ["descricao"]
        fields = ["id", "descricao"]


class IndicadorResource(resources.ModelResource):

    class Meta:
        model = Indicador
        import_id_fields = ["id"]
        fields = ["id", "descricao", "tipo"]
