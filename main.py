from flask import Flask, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__)

# Configure Selenium Chrome WebDriver
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-default-apps")


    # Use Chromium binary installed via apk
    options.binary_location = "/usr/bin/chromium-browser"

    # Set Chromedriver path
    service = Service("/usr/bin/chromedriver")
    
    return webdriver.Chrome(service=service, options=options)

# Scrape Duolingo stats
def get_duolingo_stats(username):
    url = f"https://www.duolingo.com/profile/{username}"
    driver = get_driver()

    try:
        driver.get(url)
        time.sleep(5)

        # Scroll down to ensure content loads
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Streak
        try:
            streak_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[4]/div[2]/div/div[1]/div/div/h4"))
            )
            streak = streak_element.text
        except:
            streak = "Not Found"

        # XP
        try:
            xp_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[4]/div[2]/div/div[2]/div/div/h4"))
            )
            xp = xp_element.text
        except:
            xp = "Not Found"

        return {"username": username, "streak": streak, "xp": xp}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

@app.route("/duolingo/<username>")
def duolingo(username):
    return jsonify(get_duolingo_stats(username))

@app.route("/widget/<username>")
def widget(username):
    data = get_duolingo_stats(username)
    return render_template("widget.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

