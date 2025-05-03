from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    # Basic profile
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    interests = models.JSONField(blank=True, null=True, help_text="List of user interests/tags")
    is_premium = models.BooleanField(default=False)
    onboarding_complete = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    metadata = models.JSONField(blank=True, null=True, help_text="Additional user metadata")

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username or self.email

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