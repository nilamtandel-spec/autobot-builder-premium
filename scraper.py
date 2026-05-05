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

        title = soup.title.string.strip() if soup.title else "Website Bot"
        text = " ".join(soup.get_text(separator=" ").split())

        # IMPORTANT: if website blocked
        if len(text) < 200:
            text = "Website content could not be extracted properly."

        return {
            "title": title,
            "content": text[:20000],
            "pages": [url]
        }

    except Exception as e:
        return {
            "title": "Website Bot",
            "content": f"Error: {str(e)}",
            "pages": [url]
        }
