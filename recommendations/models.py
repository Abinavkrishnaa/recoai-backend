from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.username

class Content(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    embedding = models.JSONField()
    content_type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)