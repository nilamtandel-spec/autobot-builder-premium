import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers, timeout=15)

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else "Website Bot"

        text = soup.get_text(separator=" ")
        clean_text = " ".join(text.split())

        if len(clean_text) < 100:
            clean_text = "Website content could not be extracted properly."

        return {
            "title": title,
            "content": clean_text[:30000],
            "pages": [url]
        }

    except Exception as e:
        return {
            "title": "Website Bot",
            "content": f"Error fetching website: {str(e)}",
            "pages": [url]
        }
