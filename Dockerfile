# Use a full Python version (not slim)
FROM python:3.9

WORKDIR /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up Chrome & Chromedriver
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
