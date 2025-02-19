import socket

HOST = "127.0.0.1"
PORT = 54033

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        data_to_send = input("Message to send:").strip()
        if not data_to_send:
            print("Пустое сообщение не отправляется")
            continue
        data_bytes_send = data_to_send.encode()
        try:
            sock.sendall(data_bytes_send)
        except ConnectionError:
            print("Не удалось отправить сообщение сервер отключен")
            break
        if data_to_send.lower() in ["exit"]:
            print("Клиент завершает работу")
            break
        if data_to_send.lower() in ["stop server"]:
            print("Вы завершили работу сервера")
        try:
            data_bytes_received = sock.recv(1024)
            if not data_bytes_received:
                print("Сервер отключился")
                break

            data_received = data_bytes_received.decode()
            print("Received:", data_received)
        except ConnectionError:
            print("Программа на вашем хост-компьютере разорвала установленное подключение")
            break
