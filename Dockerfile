FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG False

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

# Create static directory if it doesn't exist
RUN mkdir -p static

# Collect static files with verbose output to see what's happening
RUN python manage.py collectstatic --noinput -v 2

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "roteiro_ibiapaba.wsgi:application"]