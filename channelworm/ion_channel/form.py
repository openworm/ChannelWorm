from django.forms import ModelForm
from django import forms
from models import Experiment, Reference


# class GraphForm(ModelForm):
#     class Meta:
#         model = Experiment
#         fields = '__all__'
#         localized_fields = '__all__'
#         # widgets = {
#         #     'doi': forms.TextInput(attrs={'class': "form-control"})
#         # }

class ReferenceForm(ModelForm):
    class Meta:
        model = Reference
        exclude = ('username','create_date')


class PubForm(forms.Form):
    DOI = forms.CharField(max_length=100,required=False,label='Search by DOI')
    PMID = forms.IntegerField(required=False,label='Search by PMID')
