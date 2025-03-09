from flask import Flask, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

def get_duolingo_stats(username):
    url = f"https://www.duolingo.com/profile/{username}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use built-in Chrome & Chromedriver (inside container)
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)

        # Wait for Streak element
        try:
            streak_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[4]/div[2]/div/div[1]/div/div/h4"))
            )
            streak = streak_element.text
        except:
            streak = "Not Found"

        # Wait for XP element
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
