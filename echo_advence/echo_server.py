import socket

HOST = "127.0.0.1"
PORT = 54033

if __name__ == '__main__':

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen()

        while True:
            print("Ожидаю подключение...")
            sock, addr = serv_sock.accept()
            with sock:
                print("Подключение по", addr)

                while True:
                    try:
                        data = sock.recv(1024)
                        if not data:
                            print(f"Клиент {addr} отключился")
                            break

                        data_str = data.decode().strip()
                        print(f'Received: {data}, from {addr}')
                        if data_str.lower() == "exit":
                            print(f"клиент {addr} запросил отключение.")
                            break
                        elif data_str.lower() == "stop server":
                            print("Сервер выключен по запросу клиента")
                            sock.close()
                            serv_sock.close()
                            break

                        data = data_str.upper().encode()

                        print(f'Send: {data}, to {addr}')
                        sock.sendall(data)
                    except ConnectionError:
                        print(f"Клиент внезапно отключился")
                        break

                print("Отключение по", addr)
