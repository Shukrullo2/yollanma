from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message, custom_email_validator
from django import forms


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(validators=[custom_email_validator])
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
            'social_linkedin': 'Link to LinkedIn Profile',
            'social_instagram': 'Link to Instagram Profile',
            'social_telegram': 'Link to Telegram Profile',
            'social_github': 'Link to GitHub Profile',
            'social_website': 'Link to Website',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = {'name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_pic',
                  'social_github', 'social_instagram', 'social_linkedin', 'social_telegram',
                  'social_website',
                  }
        labels = {
            'first_name': 'Name',
            'social_linkedin': 'Link to LinkedIn Profile',
            'social_instagram': 'Link to Instagram Profile',
            'social_telegram': 'Link to Telegram Profile',
            'social_github': 'Link to GitHub Profile',
            'social_website': 'Link to Website',
        }
    order = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_pic',
                  'social_github', 'social_instagram', 'social_linkedin', 'social_telegram',
                  'social_website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        self.fields = {key: self.fields[key] for key in self.order}

class CustomProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = {'user_type'}

    def __init__(self, *args, **kwargs):
        super(CustomProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = {'description', 'name'}

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = {'email', 'subject', 'body', 'attached'}

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})