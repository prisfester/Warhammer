import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote

# ==========================================
# PARTNER-ADS KONFIGURATION
# Indtast dit Partner-ID og Banners/Program-ID for butikkerne her
# ==========================================
PARTNER_ID = "57563" # Erstat med dit Partner-ads ID (f.eks. 12345)

STORES_CONFIG = {
    "Faraos Cigarer": {
        "banner_id": "1234", # Erstat med banner/program-ID for Faraos Cigarer hos Partner-ads
        "price_selector": ".price"
    },
    "Kelz0r": {
        "banner_id": "5678", # Erstat med banner/program-ID for Kelz0r hos Partner-ads
        "price_selector": ".product-price"
    }
}

# ==========================================
# PRODUKTOVERSIGT
# Her tilføjer du nemt nye produkter og deres almindelige links fremover!
# ==========================================
PRODUCTS = [
    {
        "id": "warhammer-combat-patrol-space-marines",
        "name": "Warhammer 40,000: Combat Patrol - Space Marines",
        "category": "warhammer",
        "stores": [
            {
                "store_name": "Faraos Cigarer",
                "url": "https://www.faraos.dk/games/warhammer40k/spacemarines/combat-patrol-space-marines"
            }
        ]
    }
]

def build_affiliate_link(store_name, product_url):
    """Bygger automatisk et Partner-ads affiliate link ud fra almindelig URL"""
    if store_name in STORES_CONFIG and PARTNER_ID != "DIT_PARTNER_ID":
        banner_id = STORES_CONFIG[store_name]["banner_id"]
        encoded_url = quote(product_url, safe='')
        return f"https://www.partner-ads.com/dk/klikban.php?partnerid={PARTNER_ID}&bannerid={banner_id}&htmlurl={encoded_url}"
    return product_url # Returnerer standard-link hvis Partner-ID ikke er sat endnu

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
            store_name = store["store_name"]
            store_info = STORES_CONFIG.get(store_name, {})
            price_selector = store_info.get("price_selector", ".price")
            
            try:
                response = requests.get(store["url"], headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    price_element = soup.select_one(price_selector)
                    
                    if price_element:
                        raw_price = price_element.get_text()
                        clean_price_str = re.sub(r'[^\d,.]', '', raw_price).replace(',', '.')
                        clean_price = float(clean_price_str)
                        
                        # Generer affiliate link automatisk
                        affiliate_link = build_affiliate_link(store_name, store["url"])
                        
                        prod_data["offers"].append({
                            "store": store_name,
                            "price": clean_price,
                            "link": affiliate_link
                        })
            except Exception as e:
                print(f"Fejl ved hentning fra {store_name}: {e}")
        
        prod_data["offers"].sort(key=lambda x: x["price"])
        results.append(prod_data)
        
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("Priser og affiliate-links succesfuldt opdateret!")

if __name__ == "__main__":
    scrape_prices()
