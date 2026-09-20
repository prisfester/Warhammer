import json
import requests
import urllib.parse

# Liste over dine produkter med direkte links til søgeresultater
PRODUCTS = [
    {
        "name": "Warhammer 40,000: Ultimate Starter Set",
        "offers": [
            {"store": "Faraos Cigarer", "price": 1150.00, "link": "https://www.faraos.dk/search?q=Warhammer+40000+Ultimate+Starter+Set"},
            {"store": "Kelz0r", "price": 1099.00, "link": "https://www.kelz0r.dk/dk/advanced_search_result.php?keywords=Ultimate+Starter+Set"},
            {"store": "Spilbræt", "price": 1120.00, "link": "https://spilbraet.dk/search?q=Ultimate+Starter+Set"}
        ]
    },
    {
        "name": "Warhammer 40,000: Combat Patrol - Space Marines",
        "offers": [
            {"store": "Faraos Cigarer", "price": 850.00, "link": "https://www.faraos.dk/search?q=Combat+Patrol+Space+Marines"},
            {"store": "Kelz0r", "price": 799.00, "link": "https://www.kelz0r.dk/dk/advanced_search_result.php?keywords=Combat+Patrol+Space+Marines"}
        ]
    },
    {
        "name": "Warhammer 40,000: Combat Patrol - Tyranids",
        "offers": [
            {"store": "Faraos Cigarer", "price": 850.00, "link": "https://www.faraos.dk/search?q=Combat+Patrol+Tyranids"},
            {"store": "Kelz0r", "price": 799.00, "link": "https://www.kelz0r.dk/dk/advanced_search_result.php?keywords=Combat+Patrol+Tyranids"}
        ]
    },
    {
        "name": "Warhammer 40,000: Introductory Set",
        "offers": [
            {"store": "Faraos Cigarer", "price": 420.00, "link": "https://www.faraos.dk/search?q=Warhammer+40000+Introductory+Set"},
            {"store": "Kelz0r", "price": 395.00, "link": "https://www.kelz0r.dk/dk/advanced_search_result.php?keywords=Introductory+Set"}
        ]
    },
    {
        "name": "Warhammer Age of Sigmar: Ultimate Starter Set",
        "offers": [
            {"store": "Faraos Cigarer", "price": 1150.00, "link": "https://www.faraos.dk/search?q=Age+of+Sigmar+Ultimate+Starter+Set"},
            {"store": "Kelz0r", "price": 1089.00, "link": "https://www.kelz0r.dk/dk/advanced_search_result.php?keywords=Age+of+Sigmar+Ultimate+Starter+Set"}
        ]
    },
    {
        "name": "Warhammer Age of Sigmar: Spearhead - Stormcast Eternals",
        "offers": [
            {"store": "Faraos Cigarer", "price": 850.00, "link": "https://www.faraos.dk/search?q=Spearhead+Stormcast+Eternals"},
            {"store": "Kelz0r", "price": 799.00, "link": "https://www.kelz0r.dk/dk/advanced_search_result.php?keywords=Spearhead+Stormcast+Eternals"}
        ]
    }
]

def main():
    print("Opdaterer priser i prices.json...")
    
    # Sorterer tilbud på hvert produkt så den billigste er øverst
    for prod in PRODUCTS:
        prod["offers"].sort(key=lambda x: x["price"])

    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(PRODUCTS, f, ensure_ascii=False, indent=2)

    print("Succes! Priserne er nu opdateret i prices.json.")

if __name__ == "__main__":
    main()
