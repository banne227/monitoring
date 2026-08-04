import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("PAP_SEARCH_URL")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_html(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()  # leve une exception si erreur HTTP
    return response.text

def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="item-title")
    annonces = []
    for item in items:
        name = item.get("name")
        link = f"https://www.pap.fr{item['href']}"
        if name and link:
            annonces.append({"ID": name, "link": link})
    return annonces

if __name__ == "__main__":
    html = get_html(url)
    listings = parse_listings(html)
        for listing in listings:
            print(listing)