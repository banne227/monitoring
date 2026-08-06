import os
from notifier import send_email
from storage import load_seen_ids, add_seen_id
from dotenv import load_dotenv
from scrapper import get_html, parse_listings

# Load the .env
load_dotenv()
url = os.getenv("SEARCH_URL")

def main():
    try:
        html = get_html(url)
    except requests.RequestException as e:
        print(f"Error fetching HTML: {e}")
        exit(1)

    seen_ids = load_seen_ids()

    listings = parse_listings(html)
    for listing in listings:
        if listing["ID"] not in seen_ids:
            try:
                send_email(listing)
                add_seen_id(listing["ID"])
            except Exception as e:
                print(f"Error sending email for listing {listing['ID']}: {e}")
    print("Finished processing listings.")
            
if __name__ == "__main__":
    main()