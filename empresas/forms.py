from django import forms
from django.contrib.auth.models import User

from .models import Empresa


class EmpresaForm(forms.ModelForm):

    def save(self, commit=True):
        if 'user_id' in self.initial:
            self.instance.user = User(id=self.initial['user_id'])

        return super().save(commit)

    class Meta:
        model = Empresa
        fields = [
            'nome', 'nome_razao_social', 'cnpj', 'im', 'ie', 'telefone',
            'whatsapp', 'email', 'cep', 'endereco', 'numero', 'complemento',
            'bairro', 'estado', 'cidade',
        ]