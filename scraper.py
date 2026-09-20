import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote

# ==========================================
# PARTNER-ADS KONFIGURATION
# ==========================================
PARTNER_ID = "57563"

STORES_CONFIG = {
    "Faraos Cigarer": {
        "banner_id": "1234",  # Erstat med Faraos Cigarers banner-ID fra Partner-ads
        "selectors": [".price", ".product-price", ".current-price", "span.price", ".price-wrapper"]
    },
    "Kelz0r": {
        "banner_id": "5678",  # Erstat med Kelz0rs banner-ID fra Partner-ads
        "selectors": [".price", ".product-price", "span.price", "#product-price"]
    }
}

# ==========================================
# PRODUKTOVERSIGT
# ==========================================
PRODUCTS = [
    # --- WARHAMMER 40,000 ---
    {
        "id": "warhammer-40k-ultimate-starter-set",
        "name": "Warhammer 40,000: Ultimate Starter Set",
        "category": "warhammer-40k",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammer40k/startersets/warhammer-40.000-ultimate-starter-set-en"
            },
            {
                "store_name": "Kelz0r",
                "url": "https://www.kelz0r.dk/magic/warhammer-40000-ultimate-starter-set-eng-p-26305.html"
            }
        ]
    },
    {
        "id": "warhammer-combat-patrol-space-marines",
        "name": "Warhammer 40,000: Combat Patrol - Space Marines",
        "category": "warhammer-40k",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammer40k/spacemarines/combat-patrol-space-marines"
            },
            {
                "store_name": "Kelz0r",
                "url": "https://www.kelz0r.dk/magic/warhammer-40000-combat-patrol-space-marines-p-26306.html"
            }
        ]
    },
    {
        "id": "warhammer-combat-patrol-ultimate-tyranids",
        "name": "Warhammer 40,000: Combat Patrol - Tyranids",
        "category": "warhammer-40k",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammer40k/tyranids/combat-patrol-tyranids"
            },
            {
                "store_name": "Kelz0r",
                "url": "https://www.kelz0r.dk/magic/warhammer-40000-combat-patrol-tyranids-p-26307.html"
            }
        ]
    },
    {
        "id": "warhammer-40k-introductory-set",
        "name": "Warhammer 40,000: Introductory Set",
        "category": "warhammer-40k",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammer40k/startersets/warhammer-40.000-introductory-set-en"
            }
        ]
    },

    # --- AGE OF SIGMAR ---
    {
        "id": "age-of-sigmar-ultimate-starter-set",
        "name": "Warhammer Age of Sigmar: Ultimate Starter Set",
        "category": "age-of-sigmar",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammerageofsigmar/starter-sets/warhammer-age-of-sigmar-ultimate-starter-set-en"
            }
        ]
    },
    {
        "id": "spearhead-stormcast-eternals",
        "name": "Warhammer Age of Sigmar: Spearhead - Stormcast Eternals",
        "category": "age-of-sigmar",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammerageofsigmar/stormcast-eternals/spearhead-stormcast-eternals"
            }
        ]
    }
]

def build_affiliate_link(store_name, product_url):
    """Bygger automatisk et Partner-ads affiliate link ud fra almindelig URL"""
    if store_name in STORES_CONFIG:
        banner_id = STORES_CONFIG[store_name]["banner_id"]
        encoded_url = quote(product_url, safe='')
        return f"https://www.partner-ads.com/dk/klikban.php?partnerid={PARTNER_ID}&bannerid={banner_id}&htmlurl={encoded_url}"
    return product_url

def scrape_prices():
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'da-DK,da;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    for prod in PRODUCTS:
        prod_data = {
            "id": prod["id"],
            "name": prod["name"],
            "category": prod["category"],
            "offers": []
        }
        
        for store in prod["stores"]:
            store_name = store["store_name"]
            store_info = STORES_CONFIG.get(store_name, {})
            selectors = store_info.get("selectors", [".price"])
            
            try:
                response = requests.get(store["url"], headers=headers, timeout=12)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    price_element = None
                    for sel in selectors:
                        found = soup.select_one(sel)
                        if found and re.search(r'\d', found.get_text()):
                            price_element = found
                            break
                    
                    if price_element:
                        raw_price = price_element.get_text()
                        # Udtræk tal inkl. komma/punktum
                        match = re.search(r'(\d+[\.,]?\d*)', raw_price.replace(' ', ''))
                        if match:
                            clean_price_str = match.group(1).replace(',', '.')
                            clean_price = float(clean_price_str)
                            
                            affiliate_link = build_affiliate_link(store_name, store["url"])
                            
                            prod_data["offers"].append({
                                "store": store_name,
                                "price": clean_price,
                                "link": affiliate_link
                            })
            except Exception as e:
                print(f"Fejl ved hentning fra {store_name} for {prod['name']}: {e}")
        
        prod_data["offers"].sort(key=lambda x: x["price"])
        results.append(prod_data)
        
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("Priser og affiliate-links opdateret!")

if __name__ == "__main__":
    scrape_prices()
