from django.forms import ModelForm
from .models import Project, Profile, Review, Tag
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link', 'tags', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        # self.fields['title'].widget.attrs.update({'class' : 'input', 'placeholder': 'Add Title'})

         # Get the instance of the current project being edited
        instance = kwargs.get('instance')

        # Set the queryset for the tags field based on the current project
        if instance:
            self.fields['tags'].queryset = Tag.objects.filter(project=instance)
        else:
            self.fields['tags'].queryset = Tag.objects.none()

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {'value': 'Place your vote', 'body':'Add a comment to your vote'}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



