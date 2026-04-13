import socket
import threading


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.running = True

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"[КЛИЕНТ] Подключен к серверу {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"[КЛИЕНТ] Ошибка: Не удалось подключиться к серверу {self.host}:{self.port}")
            print(f"[КЛИЕНТ] Причина: {e}")
            return False

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode("utf-8"))
            return True
        except socket.error as e:
            print(f"[КЛИЕНТ] Ошибка при отправке: {e}")
            return False

    def receive_response(self):
        try:
            response = self.client_socket.recv(1024).decode("utf-8")
            print(f"\n[ОТВЕТ СЕРВЕРА]\n{response}\n")
            return True
        except socket.error as e:
            print(f"[КЛИЕНТ] Ошибка при получении ответа: {e}")
            return False

    def stop(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()

    def run(self):
        # Запускаем поток для получения сообщений от сервера
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        try:
            while self.running:
                message = input()

                if message.lower() in ['exit', 'выход', 'quit']:
                    self.send_message("exit")
                    break

                if not message:
                    continue

                if not self.send_message(message):
                    break

        except KeyboardInterrupt:
            print("\n[КЛИЕНТ] Работа прервана пользователем")
        finally:
            self.stop()
            print("[КЛИЕНТ] Соединение закрыто")

    def receive_messages(self):
        while self.running:
            try:
                response = self.client_socket.recv(1024).decode("utf-8")
                if response:
                    print(f"\n[ОТВЕТ СЕРВЕРА]\n{response}\n")
                    print("Введите сообщение (или 'exit' для выхода): ")
                else:
                    break
            except:
                break