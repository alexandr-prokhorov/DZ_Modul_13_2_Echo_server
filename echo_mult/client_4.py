import socket

HOST = "127.0.0.1"
PORT = 54035
# Создаем сокет
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Подключаемся к серверу по хосту и порту.
    sock.connect((HOST, PORT))
    while True:
        # Создаем поле ввода сообщений для отправки серверу.
        data_to_send = input("Message to send:").strip()
        # Исключаем ошибку с зависанием сервера при попытке отправить пустое сообщение.
        if not data_to_send:
            print("Пустое сообщение не отправляется")
            continue
        # Преобразуем сообщение клиенты в байты для отправки на сервер.
        data_bytes_send = data_to_send.encode()
        try:
            # Создаем исключение если сервер отключен, при попытке клиента отправить сообщение.
            sock.sendall(data_bytes_send)
        except ConnectionError:
            print("Не удалось отправить сообщение сервер отключен")
            break
        # Создаем условие отключение клиента командой exit
        if data_to_send.lower() in ["exit"]:
            print("Клиент завершает работу")
            break
        # Создаем условие отключение сервера командой клиента stop server
        if data_to_send.lower() in ["stop server"]:
            print("Вы завершили работу сервера")
        try:
            # Создаем исключение на попытку клиента получить данные от выключенного сервера.
            data_bytes_received = sock.recv(1024)
            if not data_bytes_received:
                print("Сервер отключился")
                break
            # Преобразуем сообщение от сервера из байтов в строку.
            data_received = data_bytes_received.decode()
            print("Received:", data_received)
        except ConnectionError:
            print("Программа на вашем хост-компьютере разорвала установленное подключение")
            break
