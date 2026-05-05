import re

def get_answer(question, content, website_url=""):
    q = question.lower().strip()

    if q in ["hi", "hello", "hii", "hey"]:
        return "Hello! I am your website assistant. You can ask me about courses, fees, admission, contact, or other website details."

    if not content or len(content) < 50:
        return "Website content was not scanned properly. Please generate chatbot again with another website URL."

    # Direct keyword fallback for college/university website
    keywords = ["aerospace", "b.tech", "btech", "engineering", "course", "courses", "admission", "fees", "contact"]

    if any(k in q for k in keywords):
        return content[:900]

    sentences = re.split(r"[.!?]", content)
    words = [w for w in re.findall(r"\w+", q) if len(w) > 2]

    results = []
    for sentence in sentences:
        s = sentence.strip()
        s_lower = s.lower()
        score = sum(1 for word in words if word in s_lower)

        if score > 0:
            results.append((score, s))

    results.sort(reverse=True, key=lambda x: x[0])

    if results:
        return " ".join([r[1] for r in results[:4]])[:900]

    return content[:900]
