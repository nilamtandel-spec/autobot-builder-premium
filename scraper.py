import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 AutoBotBuilder/1.0"
}

def clean_text(text):
    return " ".join(text.split())

def scrape_single_page(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "Website Bot"
    text = clean_text(soup.get_text(separator=" "))

    links = []
    base_domain = urlparse(url).netloc

    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        parsed = urlparse(href)

        if parsed.netloc == base_domain and parsed.scheme in ["http", "https"]:
            clean_url = href.split("#")[0]
            links.append(clean_url)

    return title, text, list(dict.fromkeys(links))

def scrape_website(start_url, max_pages=5):
    visited = set()
    to_visit = [start_url]
    all_text = []
    page_list = []
    website_title = "Website Bot"

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            title, text, links = scrape_single_page(url)

            if len(visited) == 0:
                website_title = title

            visited.add(url)
            page_list.append(url)
            all_text.append(f"Page URL: {url}\n{text}")

            for link in links:
                if link not in visited and len(to_visit) < max_pages * 2:
                    to_visit.append(link)

        except Exception as e:
            if len(visited) == 0:
                all_text.append(f"Could not scan website. Error: {str(e)}")

    final_content = "\n\n".join(all_text)

    return {
        "title": website_title,
        "content": final_content[:30000],
        "pages": page_list
    }
