from django.core.management.base import BaseCommand
from recommendations.models import User, Content, UserInteraction
import random
import numpy as np
class Command(BaseCommand):
    help = 'Seed test data for recommendations'

    def handle(self, *args, **options):
        users = []
        for i in range(1, 6):
            username = f'user_{i}'
            email = f'user_{i}@example.com'
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpass123'
                )
            users.append(user)

        contents = []
        for i in range(1, 21):
            title = f'Content {i}'
            if Content.objects.filter(title=title).exists():
                content = Content.objects.get(title=title)
            else:
                content = Content.objects.create(
                    title=title,
                    description=f'Description for content {i}',
                    content_type='article',
                    embedding=list(np.random.rand(128).astype(float))
                )
            contents.append(content)

        for user in users:
            for content in random.sample(contents, 5):
                UserInteraction.objects.create(
                    user=user,
                    content=content,
                    interaction_type='rating',
                    rating=random.uniform(1, 5)
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))