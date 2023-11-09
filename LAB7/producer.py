import pika
import re
import requests
from bs4 import BeautifulSoup

base_url = "https://999.md"
url_template = f"{base_url}/ro/list/real-estate/apartments-and-rooms"

start_page = 1
max_page = 1

processed_urls = set()

def build_url(page):
    return f"{url_template}?page={page}"

def extract_and_push_to_queue(page_url, page, channel):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        if href and re.search(r'/ro/\d+', href):
            abs_url = f"{base_url}{href}"
            
            # Check if the URL has been processed already
            if abs_url not in processed_urls:
                processed_urls.add(abs_url)
                channel.basic_publish(
                    exchange='',
                    routing_key='product_urls',
                    body=abs_url
                )

def main(page=start_page):
    if page > max_page:
        return

    page_url = build_url(page)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='product_urls')

    extract_and_push_to_queue(page_url, page, channel)
    print(f"Extracted and pushed URLs from page {page}")

    connection.close()
    main(page + 1)

if __name__ == '__main__':
    with open('urls.txt', 'w') as file:
        file.write("")
    main()
