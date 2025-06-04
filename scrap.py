import requests
from bs4 import BeautifulSoup
import csv
import os
import time

# Create folder for images
IMAGE_DIR = "hotel_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# List of Tripadvisor hotel listing URLs for different Indian cities
city_urls = {
    "Delhi": "https://www.tripadvisor.in/Hotels-g304551-New_Delhi_National_Capital_Territory_of_Delhi-Hotels.html",
    "Mumbai": "https://www.tripadvisor.in/Hotels-g304554-Mumbai_Maharashtra-Hotels.html",
    "Bangalore": "https://www.tripadvisor.in/Hotels-g297628-Bengaluru_Karnataka-Hotels.html",
    "Jaipur": "https://www.tripadvisor.in/Hotels-g304555-Jaipur_Rajasthan-Hotels.html",
    "Goa": "https://www.tripadvisor.in/Hotels-g297604-Goa-Hotels.html",
    "Hyderabad": "https://www.tripadvisor.in/Hotels-g297586-Hyderabad_Telangana-Hotels.html",
    "Kolkata": "https://www.tripadvisor.in/Hotels-g304558-Kolkata_West_Bengal-Hotels.html",
    "Chennai": "https://www.tripadvisor.in/Hotels-g304556-Chennai_Tamil_Nadu-Hotels.html",
    "Kochi": "https://www.tripadvisor.in/Hotels-g297633-Kochi_Kerala-Hotels.html",
    "Udaipur": "https://www.tripadvisor.in/Hotels-g297672-Udaipur_Rajasthan-Hotels.html",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/90.0.4430.212 Safari/537.36"
}

def download_image(url, filepath):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"Downloaded image: {filepath}")
            return True
    except Exception as e:
        print(f"Failed to download {url} - {e}")
    return False

def scrape_hotels():
    hotels = []
    hotel_id = 1

    for city, url in city_urls.items():
        print(f"\nScraping hotels from {city} ...")
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            # Find hotel cards
            cards = soup.find_all("div", class_="listing_title")
            if not cards:
                print(f"No hotel listings found for {city}.")
                continue

            for card in cards[:15]:  # limit 15 hotels per city
                try:
                    name = card.get_text(strip=True)
                    hotel_page_link = "https://www.tripadvisor.in" + card.find("a")["href"]

                    # Visit hotel page to get description and image
                    hotel_page = requests.get(hotel_page_link, headers=HEADERS, timeout=10)
                    hotel_soup = BeautifulSoup(hotel_page.text, "html.parser")

                    # Description extraction (may vary; fallback used)
                    desc_tag = hotel_soup.find("div", class_="fIrGe _T")
                    description = desc_tag.get_text(strip=True) if desc_tag else "Description not available."

                    # Image extraction
                    img_tag = hotel_soup.find("img", class_="basicImg")
                    if img_tag and img_tag.has_attr("data-lazyurl"):
                        image_url = img_tag["data-lazyurl"]
                    elif img_tag and img_tag.has_attr("src"):
                        image_url = img_tag["src"]
                    else:
                        image_url = None

                    # Download image locally
                    image_filename = None
                    if image_url:
                        ext = image_url.split('.')[-1].split('?')[0]  # Get extension without query params
                        image_filename = f"hotel_{hotel_id}.{ext}"
                        image_path = os.path.join(IMAGE_DIR, image_filename)
                        success = download_image(image_url, image_path)
                        if not success:
                            image_filename = None
                    else:
                        print(f"No image found for hotel: {name}")

                    # Fake price logic: just a placeholder
                    price_per_night = round(2000 + hotel_id * 15, 2)

                    hotels.append({
                        "id": hotel_id,
                        "name": name,
                        "description": description,
                        "location": city,
                        "price_per_night": price_per_night,
                        "image": image_filename if image_filename else ""
                    })

                    hotel_id += 1
                    time.sleep(1)  # polite pause between requests
                except Exception as e:
                    print(f"Error processing hotel card: {e}")

        except Exception as e:
            print(f"Failed to scrape city {city}: {e}")

    return hotels

def save_to_csv(hotels):
    keys = ["id", "name", "description", "location", "price_per_night", "image"]
    with open("hotels_india.csv", "w", newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(hotels)
    print("\nCSV file 'hotels_india.csv' saved with hotel data.")

if __name__ == "__main__":
    scraped_hotels = scrape_hotels()
    save_to_csv(scraped_hotels)
