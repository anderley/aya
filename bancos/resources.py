from import_export import resources

from .models import Banco


class BancosResource(resources.ModelResource):

    class Meta:
        model = Banco
        import_id_fields = ['nome']
        fields = ['id', 'nome']
