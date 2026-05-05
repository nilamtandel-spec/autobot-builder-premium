def get_answer(question, content, website_url=""):
    question = question.lower()

    if not content or "Error fetching website" in content:
        return "Sorry, I could not fetch website content properly."

    return content[:700]
