from django.forms import ModelForm

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
