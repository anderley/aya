from django import forms
from django.contrib.auth.models import User

from .models import Fornecedor


class FornecedorForm(forms.ModelForm):

    def save(self, commit=True):
        if 'user_id' in self.initial:
            self.instance.user = User(id=self.initial['user_id'])

        return super().save(commit)

    class Meta:
        model = Fornecedor
        fields = [
            'nome', 'nome_razao_social', 'cpf_cnpj', 'im', 'ie', 'telefone',
            'whatsapp', 'email', 'cep', 'endereco', 'numero', 'complemento',
            'bairro', 'estado', 'cidade',
        ]