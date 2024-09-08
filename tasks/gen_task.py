from django.core.management.base import BaseCommand
from tasks.models import Task
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Generate random tasks'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(25000):
            Task.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                status=random.choice(['pending', 'in_progress', 'completed'])
            )
        self.stdout.write(self.style.SUCCESS('Successfully generated 25,000 tasks'))
