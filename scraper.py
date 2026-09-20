import requests
from bs4 import BeautifulSoup
import json
import re

# Liste over produkter og butikker der skal overvåges
PRODUCTS = [
    {
        "id": "warhammer-combat-patrol-space-marines",
        "name": "Warhammer 40,000: Combat Patrol - Space Marines",
        "category": "warhammer",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammer40k/spacemarines/combat-patrol-space-marines",
                "affiliate_link": "https://www.partner-ads.com/dk/klikban.php?partnerid=DIT_ID&bannerid=XXX&htmlurl=https://www.faraos.dk/games/warhammer40k/spacemarines/combat-patrol-space-marines",
                "price_selector": ".price"
            }
        ]
    }
]

def scrape_prices():
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for prod in PRODUCTS:
        prod_data = {
            "id": prod["id"],
            "name": prod["name"],
            "category": prod["category"],
            "offers": []
        }
        
        for store in prod["stores"]:
            try:
                response = requests.get(store["url"], headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    price_element = soup.select_one(store["price_selector"])
                    
                    if price_element:
                        raw_price = price_element.get_text()
                        # Udtræk tal og konverter til decimaltal
                        clean_price_str = re.sub(r'[^\d,.]', '', raw_price).replace(',', '.')
                        clean_price = float(clean_price_str)
                        
                        prod_data["offers"].append({
                            "store": store["store_name"],
                            "price": clean_price,
                            "link": store["affiliate_link"]
                        })
            except Exception as e:
                print(f"Fejl ved hentning fra {store['store_name']}: {e}")
        
        # Sorter tilbud så billigste er øverst
        prod_data["offers"].sort(key=lambda x: x["price"])
        results.append(prod_data)
        
    # Gem resultatet direkte i prices.json
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("Priser succesfuldt opdateret!")

if __name__ == "__main__":
    scrape_prices()
