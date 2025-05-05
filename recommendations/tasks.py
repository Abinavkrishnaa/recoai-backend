from celery import shared_task
from .models import  UserInteraction

@shared_task
def retrain_model():
    interaction = UserInteraction.objects.all()
    return "Model retrained successfully"