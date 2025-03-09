# Use an image that already includes Chrome & Chromedriver
FROM selenium/standalone-chrome:latest

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Start the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
