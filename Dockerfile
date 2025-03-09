# Use Alpine Linux with full Python 3
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install system dependencies (Chrome, Chromedriver, and Python tools)
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    bash \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
