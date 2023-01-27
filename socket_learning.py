import socket


URLS = {
    '/': 'Hello world',
    '/blog': 'Blog page'
}


def generate_headers(method, url):
    if method != "GET":
        return "HTTP/1.1 405 Method not allowed\n\n", 405
    if url not in URLS:
        return "HTTP/1.1 404 Not found\n\n", 404
    return "HTTP/1.1 200 OK\n\n", 200


def generate_content(status_code, url):
    if status_code == 404:
        return "<h1>Page not found</h1>"
    if status_code == 405:
        return "<h1>Method not allowed</h1>"
    return f"<h1> {URLS[url]} </h1>"


def generate_response(request):
    method, url, _ = request.split(' ', 2)  # method = "GET", url = "/"
    headers, status_code = generate_headers(method, url)
    body = generate_content(status_code, url)
    return headers + body


def run():
    # Starting IPv4 server (AF_INET -> IPv4, SOCK_STREAM -> TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set server socket option: Reuse address = True
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Start on 127.0.0.1 : 5000
    server.bind(("localhost", 5000))
    # Listening for incoming requests
    server.listen()

    while True:
        # If the server receives a request, we'll get a client_socket and client_address
        client_socket, client_address = server.accept()
        # Receive 1024 bytes
        request = client_socket.recv(1024)  # 1024 - bytes

        # Printing info about a request
        print(request)
        print(client_address)

        # If request isn't empty
        if request:
            # Generate a response
            response = generate_response(request.decode())

            # Send to a client response
            client_socket.sendall(response.encode())
            # Closing a connection
            client_socket.close()


if __name__ == "__main__":
    run()
