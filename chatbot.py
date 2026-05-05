def get_answer(question, content):
    question = question.lower()

    if not content or "Error" in content:
        return "Sorry, I could not fetch website content properly."

    if "course" in question:
        return content[:500]

    if "fee" in question or "price" in question:
        return content[:500]

    if "contact" in question:
        return content[:500]

    # smart fallback
    return content[:500]
