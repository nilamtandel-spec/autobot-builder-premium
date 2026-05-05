from flask import Flask, render_template, request, jsonify, redirect
from scraper import scrape_website
from chatbot import get_answer
import uuid

app = Flask(__name__)
BOT_STORE = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    website_url = request.form.get("url", "").strip()

    if not website_url:
        return redirect("/")

    if not website_url.startswith(("http://", "https://")):
        website_url = "https://" + website_url

    result = scrape_website(website_url)

    bot_id = str(uuid.uuid4())[:8]

    BOT_STORE[bot_id] = {
        "url": website_url,
        "title": result.get("title", "Website Bot"),
        "content": result.get("content", ""),
        "pages": result.get("pages", [website_url]),
        "chat_history": []
    }

    return redirect(f"/dashboard/{bot_id}")

@app.route("/dashboard/<bot_id>")
def dashboard(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return redirect("/")
    return render_template("dashboard.html", bot=bot, bot_id=bot_id)

@app.route("/chatbot/<bot_id>")
def chatbot_page(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return redirect("/")
    return render_template("chatbot.html", bot=bot, bot_id=bot_id)

@app.route("/api/chat/<bot_id>", methods=["POST"])
def chat(bot_id):
    bot = BOT_STORE.get(bot_id)
    if not bot:
        return jsonify({"answer": "Bot not found. Please generate chatbot again."})

    data = request.get_json() or {}
    question = data.get("question", "").strip()

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
        return redirect("/")
    return render_template("history.html", bot=bot, bot_id=bot_id)

if __name__ == "__main__":
    app.run(debug=True)
