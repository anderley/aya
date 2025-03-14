from import_export import resources

from .models import Categoria


class CategoriasResource(resources.ModelResource):

    class Meta:
        model = Categoria
        import_id_fields = ['descricao']
        fields = ['id', 'descricao']
