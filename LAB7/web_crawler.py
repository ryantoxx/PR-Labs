import re
import requests
from bs4 import BeautifulSoup

base_url = "https://999.md"
max_page = 1

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

    if page < max_page:
        next_page_url = build_url(page + 1)
        parse_page(next_page_url, page + 1)

if __name__ == '__main__':
    with open('urls.txt', 'w') as file:
        file.write("")
    start_page = 1
    parse_page(build_url(start_page), start_page)


