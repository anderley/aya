from import_export import resources

from .models import TipoLancamento


class TipoLancamentosResource(resources.ModelResource):

    class Meta:
        model = TipoLancamento
        import_id_fields = ["descricao"]
        fields = ["id", "descricao"]
