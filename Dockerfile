# Use the official Python image from the Docker Hub
FROM python:3.11.11

# Set envirenment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install all requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]
