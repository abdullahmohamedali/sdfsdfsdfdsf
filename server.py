from flask import Flask, render_template, jsonify
import your_script  # Replace this with the actual Python script filename (without .py)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("widget.html")

@app.route("/duolingo")
def get_duolingo_data():
    data = your_script.get_duolingo_stats()  # Replace with the function that gets data
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

