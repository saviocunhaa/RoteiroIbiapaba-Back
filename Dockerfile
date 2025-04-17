FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False
ENV DJANGO_SUPERUSER_USERNAME admin
ENV DJANGO_SUPERUSER_EMAIL admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD admin123

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create a script to run migrations, create superuser, and start the server
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python create_superuser.py\n\
python manage.py collectstatic --noinput\n\
gunicorn --bind 0.0.0.0:8000 roteiro_ibiapaba.wsgi:application\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the script
CMD ["/app/start.sh"]