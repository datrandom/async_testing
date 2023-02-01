import socket
from select import select


# Запуск Сервера -----------------------------------------------------
# Starting IPv4 server (AF_INET -> IPv4, SOCK_STREAM -> TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set server socket option: Reuse address = True
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Start on 127.0.0.1 : 5000
server_socket.bind(("localhost", 5000))
# Listening for incoming requests
server_socket.listen()

# Список для мониторинга состояний -----------------------------------
to_monitor = []


# Принимает соединение и добавляет клиентский сокет в список
def accept_connections(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"New connection - {client_address}")

    to_monitor.append(client_socket)


# Принимает клиентский сокет => получает запрос => отправляет ответ / закрывает соединение, если запроса нету
def live_connection(client_socket):
    request = client_socket.recv(4096)
    if request:
        response = "Hello world!\n".encode()
        client_socket.send(response)
    else:
        client_socket.close()


# Вечный цикл в котором мониторятся состояния сокетов
def event_loop():
    while True:
        # Функция select возвращает сокеты у которых изменилось состояние и они готовы к чтению
        ready_to_read, _, _ = select(to_monitor, [], [])  # read, write, errors

        # Появляется сокет который готов к чтению
        for sock in ready_to_read:
            # Если изменилось состояние серверного сокета
            if sock is server_socket:
                # Принимает соединение и добавляет клиентский сокет к мониторингу
                accept_connections(server_socket)
            # Если изменилось состояние клиентского сокета
            else:
                # Принимает запрос от клиентского сокета
                live_connection(sock)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
