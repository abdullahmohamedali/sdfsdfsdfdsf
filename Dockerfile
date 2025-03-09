# Use a Python base image that supports Railway
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install required dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Flask port (5000)
EXPOSE 5000

# Start the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
