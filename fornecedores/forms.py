from django import forms

from .models import Fornecedor


class FornecedorForm(forms.ModelForm):

    def save(self, commit=True):
        if 'tenant_id' in self.initial:
            self.instance.tenant_id = id=self.initial['tenant_id']

        return super().save(commit)

    class Meta:
        model = Fornecedor
        fields = [
            'nome', 'nome_razao_social', 'cpf_cnpj', 'im', 'ie', 'telefone',
            'whatsapp', 'email', 'cep', 'endereco', 'numero', 'complemento',
            'bairro', 'estado', 'cidade',
        ]