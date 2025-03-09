import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from flask import Flask

app = Flask(__name__)

def get_driver():
    # Install Chrome and ChromeDriver automatically
    chromedriver_autoinstaller.install()

    # Set Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Start WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route("/")
def index():
    driver = get_driver()
    driver.get("https://www.google.com")
    page_title = driver.title
    driver.quit()
    return f"Google Page Title: {page_title}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
