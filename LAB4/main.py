import socket
import signal
import sys
import threading
import json
from time import sleep

f = open('products.json')
products = json.load(f)

# Define the server's IP address and port
HOST = '127.0.0.1' # IP address to bind to (localhost)
PORT = 8080 # Port to listen on

# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

# Function to handle client requests
def handle_request(client_socket):

    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]

    response_content = ''
    status_code = 200

    if path == '/':
        sleep(5)
        response_content = 'homepage'
    elif path == '/about':
        response_content = 'about us'
    elif path == '/contacts':
        response_content = 'contacts'
    elif path == '/product':
        response_content = "<h1>The list of products:</h1>"
        for num, product in enumerate(products):
            response_content += f'<p><a href="/product/{num}">Product {num}</a></p>'

    elif path.startswith('/product/'):
        try:
            product_id = int(path.split('/')[2])
            product = products[product_id]

            response_content = f"<h1>{product['name']}</h1>"
            response_content += f"<p1 >Author: {product['author']}</p1>"
            response_content += f"<p2>Price: ${product['price']}</p2>"
            response_content += f"<p3>Description: {product['description']}</p3>"

        except (ValueError, IndexError):
            response_content = '404 Not Found'
            status_code = 404

    else:
        response_content = '404 Not Found'
        status_code = 404

    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    client_socket.close()

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:

    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    
    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()
    
    
    
    
