from django import forms
from principal.models import Metas


# CLASSE FORMULÁRIO PARA CADASTRAR AS METAS
class MetasForm(forms.ModelForm):
    class Meta:
        model = Metas
        fields = ['descricao', 'data_meta']