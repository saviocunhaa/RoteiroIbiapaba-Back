import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roteiro_ibiapaba.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Define superuser credentials
DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Create superuser if it doesn't exist
if not User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists():
    User.objects.create_superuser(
        username=DJANGO_SUPERUSER_USERNAME,
        email=DJANGO_SUPERUSER_EMAIL,
        password=DJANGO_SUPERUSER_PASSWORD
    )
    print(f'Superuser {DJANGO_SUPERUSER_USERNAME} created successfully!')
else:
    print(f'Superuser {DJANGO_SUPERUSER_USERNAME} already exists.')