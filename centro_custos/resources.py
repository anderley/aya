from import_export import resources

from .models import CentroCusto


class CentroCustosResource(resources.ModelResource):

    class Meta:
        model = CentroCusto
        import_id_fields = ['descricao']
        fields = ['id', 'descricao']
