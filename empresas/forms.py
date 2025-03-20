from django import forms

from .models import Empresa


class EmpresaForm(forms.ModelForm):

    def save(self, commit=True):
        if 'tenant_id' in self.initial:
            self.instance.tenant_id = self.initial['tenant_id']

        return super().save(commit)

    class Meta:
        model = Empresa
        fields = [
            'nome', 'nome_razao_social', 'cnpj', 'im', 'ie', 'telefone',
            'whatsapp', 'email', 'cep', 'endereco', 'numero', 'complemento',
            'bairro', 'estado', 'cidade',
        ]
