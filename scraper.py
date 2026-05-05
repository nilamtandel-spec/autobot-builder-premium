import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        # remove unwanted tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")

        # clean text
        clean_text = " ".join(text.split())

        return clean_text[:10000]

    except Exception as e:
        return f"Error fetching website: {str(e)}"
