import re

def get_answer(question, content, website_url=""):
    question = question.lower()

    if "error" in content.lower() or len(content) < 100:
        return "⚠️ Unable to fetch website content. Try another website."

    # Split content into sentences
    sentences = re.split(r'[.!?]', content)

    best_sentence = ""
    max_score = 0

    for sentence in sentences:
        score = 0
        sentence_lower = sentence.lower()

        for word in question.split():
            if word in sentence_lower:
                score += 1

        if score > max_score:
            max_score = score
            best_sentence = sentence

    if best_sentence.strip():
        return best_sentence.strip()

    return "Sorry, I couldn't find a relevant answer. Please check the website directly."
