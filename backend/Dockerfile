FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Create static directory
RUN mkdir -p /app/static

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Runtime env vars (injected by Railway)
ARG ENVIRONMENT
ARG DJANGO_KEY
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG ALLOWED_HOSTS
ARG CORS_ALLOWED_ORIGINS
ARG EMAIL_APP_USER
ARG EMAIL_APP_PASSWORD
ARG FRONTEND_URL
ARG API_IMG_KEY

ENV ENVIRONMENT=$ENVIRONMENT
ENV DJANGO_KEY=$DJANGO_KEY
ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS
ENV CORS_ALLOWED_ORIGINS=$CORS_ALLOWED_ORIGINS
ENV EMAIL_APP_USER=$EMAIL_APP_USER
ENV EMAIL_APP_PASSWORD=$EMAIL_APP_PASSWORD
ENV FRONTEND_URL=$FRONTEND_URL
ENV API_IMG_KEY=$API_IMG_KEY

# Create a non-root user
RUN useradd -m myuser
RUN chown -R myuser:myuser /app
USER myuser

# Expose port
EXPOSE 8000

# Run migrations and start gunicorn server
CMD sh -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput 2>/dev/null; gunicorn server.wsgi:application --bind 0.0.0.0:8000"