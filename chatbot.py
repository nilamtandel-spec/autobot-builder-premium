import re

def split_sentences(content):
    sentences = re.split(r"(?<=[.!?])\s+", content)
    return [s.strip() for s in sentences if len(s.strip()) > 40]

def score_sentence(question_words, sentence):
    sentence_lower = sentence.lower()
    score = 0

    for word in question_words:
        if len(word) > 2 and word in sentence_lower:
            score += 1

    return score

def get_answer(question, content, website_url=""):
    question_lower = question.lower()

    greetings = ["hi", "hello", "hey", "hii", "good morning", "good evening"]
    if question_lower in greetings:
        return "Hello! I am your website assistant. Ask me anything about this website."

    if not content or len(content) < 50:
        return "I could not find enough website content. Please try another URL."

    question_words = re.findall(r"\w+", question_lower)
    sentences = split_sentences(content)

    ranked = sorted(
        sentences,
        key=lambda s: score_sentence(question_words, s),
        reverse=True
    )

    best = [s for s in ranked[:4] if score_sentence(question_words, s) > 0]

    if best:
        answer = " ".join(best)
        return answer[:900] + ("..." if len(answer) > 900 else "")

    if "contact" in question_lower or "phone" in question_lower or "email" in question_lower:
        return "I could not find exact contact details in the scanned content. Please check the Contact page of the website."

    if "fee" in question_lower or "price" in question_lower or "cost" in question_lower:
        return "I could not find exact fee or pricing details in the scanned content. Please check the Fees/Pricing page of the website."

    return f"I could not find an exact answer from the scanned website content. You may visit the website for more details: {website_url}"
