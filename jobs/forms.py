from django.forms import ModelForm
from .models import Job
from projects.models import Tag
from django import forms

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'featured_image', 'description', 'tags', 'budget', 'duration']
        labels = {
            'budget': 'Budget in soums',
            'duration': 'Duration in days'
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