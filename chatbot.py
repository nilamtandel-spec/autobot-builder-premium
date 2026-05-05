def get_answer(question, content, website_url=""):
    question = question.lower()

    if "error" in content.lower() or len(content) < 100:
        return "⚠️ Unable to fetch website content. Try another website."

    if "course" in question:
        return content[:600]

    if "fee" in question or "price" in question:
        return content[:600]

    if "contact" in question:
        return content[:600]

    return content[:600]
