"""
Web scraper for pimenton.com.uy catalog
This script attempts to scrape product and category data from the website.
Use this to replace the sample data in catalog_data.py with real catalog data.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
import re


class PimentonScraper:
    """Scraper for Pimenton e-commerce website"""

    def __init__(self, base_url: str = "https://pimenton.com.uy"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def get_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_categories(self) -> Dict[str, Dict]:
        """Scrape main categories and subcategories"""
        print("Scraping categories...")
        soup = self.get_page(self.base_url)

        if not soup:
            print("Failed to fetch homepage. The website might be blocking automated requests.")
            print("You may need to:")
            print("  1. Add authentication/cookies if required")
            print("  2. Use a proxy service")
            print("  3. Manually export the catalog data")
            return {}

        categories = {}

        # Try to find navigation menu (adjust selectors based on actual site structure)
        # Common patterns for e-commerce sites:
        nav_selectors = [
            'nav.main-navigation',
            'ul.menu',
            'nav.navbar',
            'div.categories',
            'ul.nav-menu',
            '.main-menu'
        ]

        for selector in nav_selectors:
            nav = soup.select_one(selector)
            if nav:
                print(f"Found navigation with selector: {selector}")
                # Extract categories from navigation
                category_items = nav.find_all(['a', 'li'])
                for item in category_items:
                    category_name = item.get_text(strip=True)
                    if category_name and len(category_name) > 2:
                        if category_name not in categories:
                            categories[category_name] = {
                                'subcategories': [],
                                'description': '',
                                'url': item.get('href', '')
                            }
                break

        if not categories:
            print("Could not find categories with standard selectors.")
            print("Please inspect the website manually and update the selectors in this script.")

        return categories

    def scrape_products(self, max_products: int = 100) -> List[Dict]:
        """Scrape product listings"""
        print(f"Scraping up to {max_products} products...")
        products = []

        # Try common product listing URLs
        listing_urls = [
            f"{self.base_url}/productos",
            f"{self.base_url}/products",
            f"{self.base_url}/tienda",
            f"{self.base_url}/shop",
            self.base_url  # Homepage might have products
        ]

        for url in listing_urls:
            print(f"Trying {url}...")
            soup = self.get_page(url)

            if not soup:
                continue

            # Common product selectors for e-commerce sites
            product_selectors = [
                'div.product',
                'div.product-item',
                'article.product',
                '.product-card',
                '.product-box',
                'div[data-product-id]'
            ]

            for selector in product_selectors:
                product_elements = soup.select(selector)
                if product_elements:
                    print(f"Found {len(product_elements)} products with selector: {selector}")

                    for elem in product_elements[:max_products]:
                        product = self._parse_product(elem)
                        if product:
                            products.append(product)

                    if products:
                        break

            if products:
                break

        return products

    def _parse_product(self, element) -> Dict:
        """Parse a product element"""
        try:
            # Try to extract product information
            # Adjust these selectors based on actual site structure
            product = {
                'name': '',
                'description': '',
                'price': 0,
                'category': '',
                'subcategory': '',
                'url': '',
                'image': '',
                'tags': []
            }

            # Name
            name_selectors = ['.product-name', '.product-title', 'h2', 'h3', '.title']
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    product['name'] = name_elem.get_text(strip=True)
                    break

            # Price
            price_selectors = ['.price', '.product-price', '.precio', 'span.price']
            for selector in price_selectors:
                price_elem = element.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract numeric value
                    price_match = re.search(r'[\d,]+', price_text.replace('.', ''))
                    if price_match:
                        product['price'] = int(price_match.group().replace(',', ''))
                    break

            # Description
            desc_selectors = ['.product-description', '.description', '.product-desc']
            for selector in desc_selectors:
                desc_elem = element.select_one(selector)
                if desc_elem:
                    product['description'] = desc_elem.get_text(strip=True)
                    break

            # URL
            link = element.find('a')
            if link and link.get('href'):
                product['url'] = link['href']
                if not product['url'].startswith('http'):
                    product['url'] = self.base_url + product['url']

            # Image
            img = element.find('img')
            if img:
                product['image'] = img.get('src', '')

            # Only return if we got at least a name
            if product['name']:
                return product

        except Exception as e:
            print(f"Error parsing product: {e}")

        return None

    def scrape_full_catalog(self, max_products: int = 100) -> Dict:
        """Scrape complete catalog"""
        print("\n" + "="*80)
        print("SCRAPING PIMENTON.COM.UY CATALOG")
        print("="*80 + "\n")

        catalog = {
            'categories': {},
            'products': [],
            'scrape_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Scrape categories
        catalog['categories'] = self.scrape_categories()

        # Add delay to be respectful
        time.sleep(2)

        # Scrape products
        catalog['products'] = self.scrape_products(max_products)

        print(f"\n✓ Scraped {len(catalog['categories'])} categories")
        print(f"✓ Scraped {len(catalog['products'])} products")

        return catalog

    def save_catalog(self, catalog: Dict, filename: str = 'scraped_catalog.json'):
        """Save catalog to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Catalog saved to {filename}")


def main():
    """Main scraping execution"""
    scraper = PimentonScraper()

    # Scrape catalog
    catalog = scraper.scrape_full_catalog(max_products=100)

    # Save to file
    scraper.save_catalog(catalog)

    # Print sample
    if catalog['products']:
        print("\n--- Sample Product ---")
        sample = catalog['products'][0]
        print(json.dumps(sample, indent=2, ensure_ascii=False))

    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Review scraped_catalog.json to verify the data")
    print("2. If scraping failed, you may need to:")
    print("   - Inspect the website HTML and update selectors")
    print("   - Handle authentication/cookies")
    print("   - Use browser automation (Selenium) instead")
    print("3. Convert scraped data to the format used in catalog_data.py")
    print("4. Run the embedding tests with real data")


if __name__ == "__main__":
    main()
