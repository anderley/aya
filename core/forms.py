from django import forms

from .models import Indicador



class IndicadorAdminForm(forms.ModelForm):
    tipo = forms.MultipleChoiceField(
        choices=Indicador.TipoIndicador.choices, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Indicador
        fields = ["descricao", "tipo"]

    def clean_tipo(self):
        return ','.join(self.cleaned_data["tipo"])