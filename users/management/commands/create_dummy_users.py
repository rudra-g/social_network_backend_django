from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    help = 'Create dummy users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for _ in range(total):
            username = f'user_{random.randint(1000, 9999)}'
            email = f'{username}@example.com'
            password = 'password123'
            User.objects.create_user(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'{total} dummy users created successfully.'))
