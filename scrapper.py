import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load the .env
load_dotenv()
url = os.getenv("SEARCH_URL")

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
        city = item.find("span", class_="h1")
        city_name = city.text.strip() if city else None
        price_tag = item.find("span", class_="item-price")
        price = price_tag.text.strip().replace("\xa0", " ") if price_tag else None
        link = f"https://www.pap.fr{item.get('href')}" if item.get("href") else None
        if name and link:
            annonces.append({"ID": name, "link": link, "price": price, "city": city_name})
    return annonces

if __name__ == "__main__":
    try:
        html = get_html(url)
    except requests.RequestException as e:
        print(f"Error fetching HTML: {e}")
        exit(1)

    listings = parse_listings(html)
    for listing in listings:
        print(listing)