from flask import Flask, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def get_duolingo_stats(username):
    url = f"https://www.duolingo.com/profile/{username}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)  # Give JavaScript time to load

        # Scroll to the bottom to ensure all content loads
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Save page source for debugging AFTER JavaScript has loaded
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Wait for Streak element
        try:
            streak_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[1]/div/div/h4"))
            )
            streak = streak_element.text
        except:
            streak = "Not Found"

        # Wait for XP element
        try:
            xp_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[3]/div[2]/div/div[2]/div/div/h4"))
            )
            xp = xp_element.text
        except:
            xp = "Not Found"

        return {
            "username": username,
            "streak": streak,
            "xp": xp
        }

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
