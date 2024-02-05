from django.db import models
from users.models import Profile
from projects.models import Tag
import uuid
from datetime import datetime

# Create your models here.


class Job(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    budget = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    tags = models.ManyToManyField(Tag, blank=True)
    click_total = models.IntegerField(default=0, null=True, blank=True)
    clicked = models.ManyToManyField(Profile, blank=True, related_name="clicked")
    assigned = models.OneToOneField(Profile, blank=True, related_name="assigned", null=True, on_delete=models.SET_NULL)
    assigned_date = models.DateTimeField(default=datetime.now)
    description = models.TextField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_done = models.BooleanField(default=False, null=True, blank=True)
    is_assigned = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created', 'title']


class Contract(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    client = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name="Client")
    freelancer = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name="Freelancer")
    title = models.CharField(max_length=200, null=True, blank=True)
    budget = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    description = models.TextField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_signed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created', 'title']