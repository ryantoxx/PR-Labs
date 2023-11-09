import pika
from tinydb import TinyDB
import threading
from data_extraction import get_data

db = TinyDB('db.json')
thread_lock = threading.Lock()


def process_url(ch, method, properties, body):
    url = body.decode('utf-8')
    data = get_data(url)

    if data:
        with thread_lock:
            db.insert(data)
        print(f"Processed URL: {url}")

def consumer_worker(consumer_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='product_urls')

    channel.basic_consume(
        queue='product_urls',
        on_message_callback=process_url,
        auto_ack=True
    )

    print(f"Consumer {consumer_id} is waiting for messages. To exit, press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consumer_count = 3
    threads = []

    for i in range(consumer_count):
        thread = threading.Thread(target=consumer_worker, args=(i,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

