FROM mcr.microsoft.com/playwright/python:v1.40.0-focal  # Full Python + Chrome

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt  # Install your dependencies


# Expose the Flask port
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
