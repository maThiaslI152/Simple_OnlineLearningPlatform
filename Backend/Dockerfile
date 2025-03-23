# Use official Python image as base
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app/Backend


# Copy and install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY . .

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run Django using Gunicorn
CMD ["gunicorn", "--chdir", "Backend/Backend", "--bind", "0.0.0.0:8000", "wsgi:application"]
