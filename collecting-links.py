import requests
from bs4 import BeautifulSoup
import random
import csv

# Base URL of Dubizzle car listings
base_url = "https://uae.dubizzle.com/search/?keyword=cars&page="

# A list of multiple User-Agent strings to avoid blocking during scraping
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/102.0.1245.44",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave/91.1.25.72 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/537.36"
]

# Function to extract car listing links from a single page
def get_car_links(page):
    url = f"{base_url}{page}"
    headers = {"User-Agent": random.choice(user_agents)}  # Rotate User-Agent to avoid blocks
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        car_links = []
        for link in soup.find_all("a", href=True):
            if "/motors/used-cars/" in link["href"]:  # Filter only car listings
                full_link = "https://uae.dubizzle.com" + link["href"]
                car_links.append(full_link)

        return car_links
    else:
        print(f"❌ Failed to retrieve page {page} (Status code: {response.status_code})")
        return []

# Loop through multiple pages and collect all car listing links
all_links = []
for page in range(2, 20):  # You can change this range to scrape more pages
    print(f"Scraping page {page}...")
    links = get_car_links(page)
    all_links.extend(links)

# Remove duplicate links if any
all_links = list(set(all_links))

# Print each collected link (Optional)
print("\nCollected Car Links:")
for link in all_links:
    print(link)

print(f"\n✅ Total unique car links found: {len(all_links)}")

# === Save links to a CSV file ===
output_file = "car_links.csv"

# Writing to CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Car Listing URL"])  # Header
    for link in all_links:
        writer.writerow([link])

print(f"\n📁 All links have been saved to '{output_file}' successfully.")
