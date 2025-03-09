# Use a base image with Chrome & Chromedriver
FROM selenium/standalone-chrome:latest

# Set the working directory
WORKDIR /app

# Copy the dependencies first
COPY requirements.txt .

# Install dependencies (including Gunicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port 5000 (instead of 8000)
EXPOSE 5000

# Start the app using Gunicorn on port 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
