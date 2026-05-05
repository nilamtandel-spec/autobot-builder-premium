import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "Website Bot"
        text = " ".join(soup.get_text(separator=" ").split())

        return {
            "title": title,
            "content": text[:30000],
            "pages": [url]
        }

    except Exception as e:
        return {
            "title": "Website Bot",
            "content": f"Error fetching website: {str(e)}",
            "pages": [url]
        }
