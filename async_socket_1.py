import socket
import selectors


# Starting IPv4 server (AF_INET -> IPv4, SOCK_STREAM -> TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set server socket option: Reuse address = True
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Start on 127.0.0.1 : 5000
server.bind(("localhost", 5000))
# Listening for incoming requests
server.listen()


# Принимает соединение: возвращает сокет клиента и ip:port
def accept_connections(server_socket):
    client_socket, client_address = server_socket.accept()
    return client_socket, client_address


# Цикл который ожидает запроса от клиента и отправляет ответ, в случае пустого запроса прерывает соединение
def live_connection(client_socket):
    while True:
        request = client_socket.recv(4096)
        if request:
            response = "Hello world!\n".encode()
            client_socket.send(response)
        else:
            break
    client_socket.close()


# Цикл который ожидает подключений к серверу, в случае нового соединения запускает цикл приема запросов
def run():
    while True:
        # Waiting for new connections
        client_socket, client_address = accept_connections(server)
        print(f"New connection - {client_address}")
        # Waiting for requests from a client
        live_connection(client_socket)


if __name__ == "__main__":
    run()
