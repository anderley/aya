from import_export import resources

from .models import MotivoExclusao


class MotivosExclusaoResource(resources.ModelResource):

    class Meta:
        model = MotivoExclusao
        import_id_fields = ["descricao"]
        fields = ["id", "descricao"]
