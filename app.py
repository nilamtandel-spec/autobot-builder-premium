from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from scraper import scrape_website
from chatbot import get_answer
import uuid

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Temporary in-memory storage for final-year demo
BOT_STORE = {}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    website_url = request.form.get("url", "").strip()

    if not website_url:
        return render_template("index.html", error="Please enter a website URL.")

    if not website_url.startswith(("http://", "https://")):
        website_url = "https://" + website_url

    result = scrape_website(website_url)

    bot_id = str(uuid.uuid4())[:8]
    BOT_STORE[bot_id] = {
        "url": website_url,
        "title": result.get("title", "Website Bot"),
        "content": result.get("content", ""),
        "pages": result.get("pages", []),
        "chat_history": []
    }

    session["bot_id"] = bot_id
    return redirect(url_for("dashboard", bot_id=bot_id))

@app.route("/dashboard/<bot_id>")
def dashboard(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return redirect(url_for("home"))

    embed_code = f'<script src="https://yourdomain.com/widget.js" data-bot-id="{bot_id}"></script>'
    return render_template("dashboard.html", bot=bot, bot_id=bot_id, embed_code=embed_code)

@app.route("/chatbot/<bot_id>")
def chatbot_page(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return redirect(url_for("home"))

    return render_template("chatbot.html", bot=bot, bot_id=bot_id)

@app.route("/api/chat/<bot_id>", methods=["POST"])
def chat(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return jsonify({"answer": "Bot not found. Please generate chatbot again."})

    data = request.get_json() or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please type your question."})

    answer = get_answer(question, bot["content"], bot["url"])

    bot["chat_history"].append({
        "question": question,
        "answer": answer
    })

    return jsonify({"answer": answer})

@app.route("/history/<bot_id>")
def history(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return redirect(url_for("home"))

    return render_template("history.html", bot=bot, bot_id=bot_id)

if __name__ == "__main__":
    app.run(debug=True)
