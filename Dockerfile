# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and extract Chromium manually (NO APT REQUIRED)
RUN curl -L https://github.com/puppeteer/puppeteer/releases/download/v21.0.0/chromium-linux64.zip -o chromium.zip && \
    unzip chromium.zip && \
    rm chromium.zip

# Set Chromium environment variables
ENV CHROMIUM_PATH="/app/chrome-linux64/chrome"
ENV CHROMEDRIVER_PATH="/app/chrome-linux64/chromedriver"
ENV PATH="/app/chrome-linux64/:$PATH"

# Copy application files
COPY . .

# Expose port 5000
EXPOSE 5000

# Run Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
