import json
import requests
from bs4 import BeautifulSoup

# Liste over webshops og deres søge-URL'er for Warhammer
STORES = [
    {
        "name": "NextLevelGames",
        "url": "https://nextlevelgames.dk/collections/warhammer-40k?page=1"
    }
]

def fetch_prices():
    products = []
    
    # Eksempel på hentning fra Shopify-baserede sider som NextLevelGames
    try:
        response = requests.get("https://nextlevelgames.dk/collections/warhammer-40k/products.json?limit=250")
        if response.status_code == 200:
            data = response.json()
            for item in data.get("products", []):
                variant = item["variants"][0]
                products.append({
                    "id": f"nlg-{item['id']}",
                    "name": item["title"],
                    "category": "40k",
                    "image": item["images"][0]["src"] if item.get("images") else "",
                    "offers": [
                        {
                            "store": "NextLevelGames",
                            "price": float(variant["price"]),
                            "link": f"https://nextlevelgames.dk/products/{item['handle']}"
                        }
                    ]
                })
    except Exception as e:
        print(f"Fejl ved hentning: {e}")

    # Gem alt til prices.json
    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"Gemte {len(products)} produkter i prices.json!")

if __name__ == "__main__":
    fetch_prices()
