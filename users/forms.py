from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message, custom_email_validator
from django.core.exceptions import ValidationError
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name','username', 'password1', 'password2']
        labels = {
            'first_name': 'Ism',
            'username': 'Foydalanuvchi nomi',
            'password1': 'Parol',
            'password2': 'Parolni qayta kiriting'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'bio', 'short_intro', 'profile_pic',
                  'social_github', 'social_instagram', 'social_linkedin', 'social_telegram',
                  'social_website', 'user_type'
                  ]
        labels = {
            'name': 'Ism',
            'username': 'Foydalanuvchi nomi',
            'location': 'Manzil',
            'short_intro': 'Qisqa bio',
            'user_type': 'Foydalanuvchi turi',
            'social_linkedin': 'LinkedIn Sahifasiga Havola',
            'social_instagram': 'Instagram Sahifasiga Havola',
            'social_telegram': 'Telegram Sahifasiga Havola',
            'social_github': 'GitHub Sahifasiga Havola',
            'social_website': 'Vebsaytga havola',
        }
    order = ['name', 'email', 'username', 'user_type', 'location', 'bio', 'short_intro', 'profile_pic',
                  'social_github', 'social_instagram', 'social_linkedin', 'social_telegram',
                  'social_website']
    
    def clean_email(self):
        super().clean()
        print('cleaned_dat: ', self.cleaned_data)
        # Check if the user_type is a certain type where you want to bypass the custom_email_validator
        user_type = self.data.get('user_type')
        print('user type: ', user_type)
        email = self.cleaned_data.get('email')
        print('email', email)
        if user_type == 'Client':
            print("Bypassing validation for Client")
            return email
        else:
            # If not, perform the custom email validation
            forbidden_strings = ['gmail', 'mail', 'yahoo', 'zoho', 'yandex']
            for forbidden_str in forbidden_strings:
                if forbidden_str in email:
                    raise ValidationError('Use your WIUT email address!')
            
        return email
    
    def __init__(self, *args, **kwargs):
        
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields = {key: self.fields[key] for key in self.order}
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
        

    
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
        labels = {
            'description': 'Tasnif',
            'name': 'Nom'
        }

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = {'email', 'subject', 'body', 'attached'}
        labels = {
            'subject': 'Mavzu', 
            'body': 'Matn',
            'attached': 'Fayl'
            
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class CheckboxForm(forms.Form):
    type_freelancer = forms.BooleanField(required=False, initial=False, label='Men frilanserman')
    type_client = forms.BooleanField(required=False, initial=False, label='Menga frilanserlar kerak')
    def clean(self):
        cleaned_data = super().clean()
        checkbox1 = cleaned_data.get('checkbox1')
        checkbox2 = cleaned_data.get('checkbox2')
       
        if checkbox1 and checkbox2:
            raise forms.ValidationError("Select only one checkbox.")

        return cleaned_data
  