from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.db.models.signals import post_save, post_delete
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator


def custom_email_validator(value):
    # Add your custom email validation logic here
    forbidden_strings = ['gmail', 'mail', 'yahoo', 'zoho', 'yandex']
    if any(forbidden_str in value for forbidden_str in forbidden_strings):
        raise ValidationError(_('Use your WIUT or company email!'))
    
# Create your models here.

class Profile(models.Model):
    user_type = models.CharField(max_length=20,  null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=500, blank=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/default.jpg')
    bio = models.TextField(blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_instagram = models.CharField(max_length=200, blank=True, null=True)
    social_telegram = models.CharField(max_length=200, blank=True, null=True)
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    is_activated =models.BooleanField(default=False)
    

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)

    # def clean_email(self):
    #     super().clean()
    #     print(self.user_type)
    #     # Check if the user_type is a certain type where you want to bypass the custom_email_validator
    #     if self.user_type == 'Client':
    #         print("Bypassing validation for Client")
    #         return self.cleaned_data['email']
    #     else:
    #         # If not, perform the custom email validation
    #         forbidden_strings = ['gmail', 'mail', 'yahoo', 'zoho', 'yandex']
    #         for forbidden_str in forbidden_strings:
    #             if forbidden_str in self.email:
    #                 raise ValidationError('Use your WIUT or company email!')
            
    #     return self.cleaned_data['email']
    
    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['-created']


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    # name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    is_read = models.BooleanField(default=False, null=True)
    attached = models.FileField(upload_to='attachments/', null=True, blank=True)
    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']