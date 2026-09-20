import json
import re
import requests
from bs4 import BeautifulSoup

# Liste over produkter og søgeord til danske Warhammer-butikker
PRODUCTS = [
    {
        "name": "Warhammer 40,000: Ultimate Starter Set",
        "search_term": "Warhammer 40000 Ultimate Starter Set"
    },
    {
        "name": "Warhammer 40,000: Combat Patrol - Space Marines",
        "search_term": "Combat Patrol Space Marines"
    },
    {
        "name": "Warhammer 40,000: Combat Patrol - Tyranids",
        "search_term": "Combat Patrol Tyranids"
    },
    {
        "name": "Warhammer 40,000: Introductory Set",
        "search_term": "Warhammer 40000 Introductory Set"
    },
    {
        "name": "Warhammer Age of Sigmar: Ultimate Starter Set",
        "search_term": "Age of Sigmar Ultimate Starter Set"
    },
    {
        "name": "Warhammer Age of Sigmar: Spearhead - Stormcast Eternals",
        "search_term": "Spearhead Stormcast Eternals"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def clean_price(price_str):
    """Trækker kun tal ud fra en prisstreng"""
    if not price_str:
        return None
    cleaned = re.sub(r'[^\d,.]', '', price_str)
    cleaned = cleaned.replace('.', '').replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return None

def scrape_faraos(search_term):
    """Scraper Faraos Cigarer"""
    try:
        url = f"https://www.faraos.dk/search?q={requests.utils.quote(search_term)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            item = soup.select_one('.product-list-item, .product-card, .product-box')
            if item:
                link_el = item.select_one('a[href]')
                price_el = item.select_one('.price, .product-price, .current-price')
                if link_el and price_el:
                    link = link_el['href']
                    if not link.startswith('http'):
                        link = 'https://www.faraos.dk' + link
                    price = clean_price(price_el.get_text())
                    if price:
                        return {"store": "Faraos Cigarer", "price": price, "link": link}
    except Exception as e:
        print(f"Fejl ved Faraos ({search_term}): {e}")
    return None

def scrape_kelz0r(search_term):
    """Scraper Kelz0r"""
    try:
        url = f"https://www.kelz0r.dk/dk/advanced_search_result.php?keywords={requests.utils.quote(search_term)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            product = soup.select_one('.productListing-even, .productListing-odd, .product-card')
            if product:
                link_el = product.select_one('a[href]')
                price_el = product.select_one('.productSpecialPrice, .price, .productListing-heading + td')
                if link_el and price_el:
                    link = link_el['href']
                    price = clean_price(price_el.get_text())
                    if price:
                        return {"store": "Kelz0r", "price": price, "link": link}
    except Exception as e:
        print(f"Fejl ved Kelz0r ({search_term}): {e}")
    return None

def main():
    results = []

    for prod in PRODUCTS:
        print(f"Søger efter: {prod['name']}...")
        offers = []

        # Hent tilbud fra butikkerne
        faraos_offer = scrape_faraos(prod['search_term'])
        if faraos_offer:
            offers.append(faraos_offer)

        kelz0r_offer = scrape_kelz0r(prod['search_term'])
        if kelz0r_offer:
            offers.append(kelz0r_offer)

        # Sorter tilbud så billigste er først
        offers.sort(key=lambda x: x['price'])

        results.append({
            "name": prod['name'],
            "offers": offers
        })

    # Gem resultaterne direkte i prices.json
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Priser gemt succesfuldt i prices.json!")

if __name__ == "__main__":
    main()
