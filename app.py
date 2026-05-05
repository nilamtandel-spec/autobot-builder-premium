from flask import Flask, render_template, request, redirect, url_for
from scraper import scrape_website
import uuid

app = Flask(__name__)

BOT_STORE = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    website_url = request.form.get("url")

    if not website_url:
        return redirect("/")

    if not website_url.startswith("http"):
        website_url = "https://" + website_url

    result = scrape_website(website_url)

    bot_id = str(uuid.uuid4())[:8]

    BOT_STORE[bot_id] = result

    # ✅ THIS IS MAIN FIX
    return redirect(f"/dashboard/{bot_id}")

@app.route("/dashboard/<bot_id>")
def dashboard(bot_id):
    bot = BOT_STORE.get(bot_id)

    if not bot:
        return redirect("/")

    return render_template("dashboard.html", bot=bot, bot_id=bot_id)

if __name__ == "__main__":
    app.run(debug=True)
