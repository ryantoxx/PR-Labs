import requests
from bs4 import BeautifulSoup
import json

urls = {
    "homepage": "http://localhost:8080/",
    "about": "http://localhost:8080/about",
    "contacts": "http://localhost:8080/contacts",
    "product0": "http://localhost:8080/product/0",
    "product1": "http://localhost:8080/product/1"
}

for page_name, url in urls.items():
    if page_name.startswith("product"):
        extract_file = f"{page_name}.json" 
    else:
        extract_file = f"{page_name}.html" 

    try:
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if page_name.startswith("product"):
                product_name_element = soup.find("h1")
                product_author_element = soup.find("p1").text.strip()
                product_price_element = soup.find("p2").text.strip()
                product_description_element = soup.find("p3").text.strip()

                product_author_element_replace = product_author_element.replace("Author: ", "")
                product_price_element_replace = float(product_price_element.replace("Price: $", ""))
                product_description_element_replace = product_description_element.replace("Description: ", "")
                
                product_data = {
                    "name": product_name_element.text.strip(),
                    "author": product_author_element_replace,
                    "price": product_price_element_replace,
                    "description": product_description_element_replace,
                }

                with open(extract_file, 'w', encoding='utf-8') as json_file:
                    json.dump(product_data, json_file, indent=4)

            else:
                with open(extract_file, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
        else:
            print(f"Failed to extract the web page. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request for {page_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {page_name}: {e}")


