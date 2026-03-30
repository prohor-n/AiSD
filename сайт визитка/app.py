from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGES_FILE = os.path.join(BASE_DIR, "messages.txt")

@app.route("/")
def index():
    return render_template("index.html", active_page="index")

@app.route("/about")
def about():
    return render_template("about.html", active_page="about")


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    success = False

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if name or email or message:
            # формируем строку для файла
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{timestamp}] NAME: {name} | EMAIL: {email} | MESSAGE: {message}\n"

            # дописываем в файл в UTF-8
            with open(MESSAGES_FILE, "a", encoding="utf-8") as f:
                f.write(line)  # файл создастся автоматически, если его нет

            success = True

    return render_template("contacts.html", active_page="contacts", success=success)

if __name__ == "__main__":
    app.run(debug=True)
