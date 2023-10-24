import re
import requests
from bs4 import BeautifulSoup

base_url = "https://999.md"
start_page = 1
max_page = 2

url_template = f"{base_url}/ro/list/real-estate/apartments-and-rooms"

def build_url(page):
    return f"{url_template}?page={page}"

def parse_page(page_url, page):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = set() 

    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        if href and re.search(r'/ro/\d+', href):
            abs_url = f"{base_url}{href}"
            links.add(abs_url)  

    with open('urls.txt', 'a') as file:
        for link in links:
            file.write(f"{link}\n")

def main():
    with open('urls.txt', 'w') as file:
        file.write("")

    for page in range(start_page, max_page + 1):
        page_url = build_url(page)
        parse_page(page_url, page)
        print(page)

if __name__ == '__main__':
    main()
