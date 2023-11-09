import requests
from bs4 import BeautifulSoup
import json

def get_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    page_title = soup.select_one("header.adPage__header h1")
    price = soup.select_one("span.adPage__content__price-feature__prices__price__value")

    characteristics = {}
    for key in ['Suprafață totală', 'Nivelul']:
        value = soup.select_one(f"span.adPage__content__features__key:-soup-contains('{key}') + span.adPage__content__features__value")
        characteristics[key] = value.text.strip() if value else "None"

    data = {
        'url': url,
        "page_title": page_title.text.strip() if page_title else "None",
        "price": price.text.strip() if price else "None",
        "characteristics": characteristics
    }

    return data

def main():
    list_data = []

    with open('urls.txt', 'r') as file:
        for url in file:
            data = get_data(url.strip())
            if data:
                list_data.append(data)

    with open('data.json', "w", encoding="utf-8") as file:
        json.dump(list_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
