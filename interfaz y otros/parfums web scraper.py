import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape data from a URL
def scrape_parfums(url, selectors):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    items = soup.select(selectors['product_container'])

    for item in items:
        title = item.select_one(selectors['title']).get_text(strip=True) if item.select_one(selectors['title']) else 'N/A'
        price = item.select_one(selectors['price']).get_text(strip=True).replace("Gs.", "").replace(".", "").replace(",", ".") if item.select_one(selectors['price']) else 'N/A'
        description = item.select_one(selectors['description']).get_text(strip=True) if selectors['description'] and item.select_one(selectors['description']) else 'N/A'
        image = item.select_one(selectors['image'])['src'] if selectors['image'] and item.select_one(selectors['image']) else 'N/A'
        
        products.append([title, price, description, image])
    
    return products

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Price', 'Description', 'Image URL'])
        writer.writerows(data)

# Main function to scrape multiple websites
def main():
    # Define URLs and CSS selectors for each site
    websites = [
        {
            "url": "https://mannah.com.py/categoria-producto/perfumes/",
            "selectors": {
                "product_container": "#__next > main > div > div > div > div:nth-child(2) > div > div",
                "title": "a.card-header h4",
                "price": "div.price-wrapper",
                "description": "a.card-header p",  # Assuming description is in a <p> tag inside the card-header
                "image": "a.card-header img"  # Assuming images are within an <img> tag inside the card-header
            }
        },
        {
            "url": "https://www.lapetisquera.com.py/CategoriaId_23/Salud-Y-Belleza-/Perfumes-.html",
            "selectors": {
                "product_container": "div.product-item",
                "title": "h3.product-name",
                "price": "div.price",
                "description": "div.product-description",  # Assuming description exists in a product-description div
                "image": "img.product-image"  # Assuming the product image is within an img tag with class product-image
            }
        },
        {
            "url": "https://www.puntofarma.com.py/categoria/2/perfumes-y-fragancias",
            "selectors": {
                "product_container": ".product-item",
                "title": ".product-item__title",
                "price": ".product-item__price",
                "description": ".product-item__description",  # Assuming description exists
                "image": ".product-item__image img"  # Assuming images are within an <img> tag inside the product-item__image
            }
        },
        {
            "url": "https://compras.macedonia.com.py/categoria-produto/perfumes/",
            "selectors": {
                "product_container": ".product-item",
                "title": ".product-item__title",
                "price": ".product-item__price",
                "description": ".product-item__description",  # Assuming description exists
                "image": ".product-item__image img"  # Assuming images are within an <img> tag inside the product-item__image
            }
        }
    ]
    
    all_data = []
    
    # Scrape each website
    for site in websites:
        print(f"Scraping {site['url']}...")
        data = scrape_parfums(site['url'], site['selectors'])
        all_data.extend(data)
    
    # Save all data to a CSV file
    save_to_csv(all_data, "perfumes_data_detailed.csv")
    print("Scraping complete. Data saved to perfumes_data_detailed.csv.")

if __name__ == "__main__":
    main()
