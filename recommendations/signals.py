from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Content
from ml.services import generate_embedding  # Implement this

@receiver(post_save, sender=Content)
def update_content_embedding(sender, instance, **kwargs):
    if not instance.embedding:
        text = f"{instance.title} {instance.description}"
        instance.embedding = generate_embedding(text)
        instance.save(update_fields=['embedding'])