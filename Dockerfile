# Use an image that already includes Chrome & Chromedriver
FROM selenium/standalone-chrome:latest

# Set the working directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
