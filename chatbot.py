import re

def get_answer(question, content, website_url=""):
    question = question.lower()

    if not content or "error fetching website" in content.lower():
        return "Sorry, I could not fetch website content properly. Please try another website."

    if "website content could not be extracted" in content.lower():
        return "This website is blocking content scanning. Please try another website."

    sentences = re.split(r"[.!?]", content)

    best_sentences = []

    question_words = question.split()

    for sentence in sentences:
        sentence_lower = sentence.lower()
        score = 0

        for word in question_words:
            if len(word) > 2 and word in sentence_lower:
                score += 1

        if score > 0:
            best_sentences.append((score, sentence.strip()))

    best_sentences.sort(reverse=True, key=lambda x: x[0])

    if best_sentences:
        answer = " ".join([s[1] for s in best_sentences[:3]])
        return answer[:900]

    return "Sorry, I could not find a relevant answer from the scanned website content."
