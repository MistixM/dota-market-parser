# Import independencies (scap libs)
import requests
import csv
from bs4 import BeautifulSoup

def main():

    # Mask request to avoud Cloudflare
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Cookie": "cf_clearance=QqMBkzeeXJaZJXDxVvezeQYBFw0sAkMta9rKctl2lE8-1715683531-1.0.1.1-piaTe6mzxzEM6n8SdL2InLmAtlaJ2aEAaIYMCRgYE6Sv1QhcpuPcEju9P0.DwjsW23wWjVUT7q12hucfpKnmqw; PHPSESSID=f211f8f03dc8173e8ed08e1b4f87e062; _csrf=iyIJrbf7RS21m-jFoJMRFvIgkf-75Qgd; goon=0; _ga=GA1.2.294339912.1715683537; _gid=GA1.2.1067126255.1715683537; _ym_uid=1715683537441124666; _ym_d=1715683537; d2mid=ikWqZUXN0mDSeTutJtscZweTLyyBkG; _ga_JBBJ0SRBZW=GS1.2.1715683537.1.1.1715683545.0.0.0"
    }

    # Open csv to save data
    with open('data.csv', 'w', encoding='utf-8') as file:
        # Create writer and write titles
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['Name', 'Price', 'Url'])

        # Send request to each page
        for page in range(178):
            # Just for debug
            print(f"[INFO] Scraping.. Page scraped: {page}", end='\r')

            # Send request to page and create bs4 object
            r = requests.get(f'https://market.dota2.net/?p={page}&sd=desc', headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Get market block with inner items
            market = soup.find('div', class_='market-items')
            
            # Get all items from this block
            items = market.find_all('a', class_='item')
            
            # Check each item and scrap inner information (name, price and url)
            for item in items:
                name = item.find('div', class_='name').text.strip()
                price = item.find('div', class_='price').text
                url = item['href'].strip()

                # Eventually save received information to CSV file
                writer.writerow([name, price, "https://market.dota2.net/en" + url])

if __name__ == "__main__":
    main()