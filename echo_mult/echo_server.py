import socket
import threading

HOST = "127.0.0.1"
PORT = 54035


def handle_connection(sock, addr):
    """
    Функция обрабатывает каждое подключение клиента.
    :param sock: Сокет для обмена данными с клиентом.
    :param addr: Адрес клиента (IP и PORT)
    """
    with sock:
        print("Подключение по", addr)
        #  with используем для автоматического закрытия сокета после завершения работы.

        while True:
            try:
                # Получаем данные от клиента. Максимальный размер данных 1024 байта.
                data = sock.recv(1024)
                # Если данные не получены. Выводим сообщение и выходим из цикла.
                if not data:
                    print(f"Клиент {addr} отключился")
                    break
                # Преобразуем данные в строку для дальнейшей обработки условий "exit","stop server"
                data_str = data.decode().strip()
                print(f"Received: {data_str}, from {addr}")
                # Создаем условие для выхода клиента и отключение сервера по запросу клиента.
                if data_str.lower() == "exit":
                    print(f'Клиент {addr} запросил отключение')
                    break
                elif data_str.lower() == "stop server":
                    print(f"Клиент {addr} запросил отключение сервера")
                    sock.sendall('Сервер выключается'.encode())
                    break
                # Преобразуем данные обратно в байты.
                data = data_str.upper().encode()
                print(f"Send: {data.decode()}, to {addr}")
                sock.sendall(data)
            # Создаем исключение отключения клиента.
            except ConnectionError:
                print(f"Клиент {addr} внезапно отключился")
                break
        print("Отключение по", addr)


if __name__ == '__main__':
    # Создаем сокет для работы.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        # Привязываем сокет к хосту и порту.
        serv_sock.bind((HOST, PORT))
        # Начинаем поиск входящим подключений.
        serv_sock.listen()
        while True:
            print('Waiting for connection...')
            try:
                my_sock, my_addr = serv_sock.accept()
                # Создаем поток для подключений клиентов. Каждый клиент в отдельном потоке.
                thread = threading.Thread(target=handle_connection, args=(my_sock, my_addr))
                thread.start()
            except ConnectionError:
                print("Сервер завершает работу")
                break
