import socket
import selectors


selector = selectors.DefaultSelector()  # <-----------------------------------------------------------------------------


def server():
    # Starting IPv4 server (AF_INET -> IPv4, SOCK_STREAM -> TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set server socket option: Reuse address = True
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Start on 127.0.0.1 : 5000
    server_socket.bind(("localhost", 5000))
    # Listening for incoming requests
    server_socket.listen()

    selector.register(fileobj=server_socket, events=selectors.EVENT_READ, data=accept_connections)  # <-----------------


def accept_connections(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"New connection - {client_address}")

    selector.register(fileobj=client_socket, events=selectors.EVENT_READ, data=live_connection)  # <--------------------


def live_connection(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = "Hello world!\n".encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)  # <-------------------------------------------------------------------------
        client_socket.close()


def event_loop():
    while True:
        events = selector.select()  # [(key, Events), (key, Events), (key, Events)...]
        # key -> SelectorKey( fileobj, events, data)
        for key, _ in events:
            callback = key.data  # callback = accept_connections/live_connection
            callback(key.fileobj)  # live_connection(client_socket)


if __name__ == "__main__":
    server()
    event_loop()
