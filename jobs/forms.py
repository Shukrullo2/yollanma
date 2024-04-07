from django.forms import ModelForm
from .models import Job, Contract
from projects.models import Tag
from django import forms

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'featured_image', 'description', 'tags', 'budget', 'duration']
        labels = {
             'title': 'Nom',
            'budget': 'Byudjet (so`mda)',
            'duration': 'Muddat (kunlarda)',
            'description': "Tasnif",
            'featured_image': 'Surat',
            'tags': 'Teglar',

        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        instance = kwargs.get('instance')

        # Set the queryset for the tags field based on the current project
        if instance:
            self.fields['tags'].queryset = Tag.objects.filter(job=instance)
        else:
            self.fields['tags'].queryset = Tag.objects.none()


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['title', 'budget', 'duration', 'description', ]
        labels = {
            'title': 'Nom',
            'budget': 'Byudjet (so`mda)',
            'duration': 'Muddat (kunlarda)',
            'description': "Tasnif"
        }
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

      