from django.forms import ModelForm

from ion_channel.models import Experiment


class GraphForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ('doi',)
        localized_fields = '__all__'
        # widgets = {
        #     'doi': forms.TextInput(attrs={'class': "form-control"})
        # }
