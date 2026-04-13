import socket
import threading

RUS_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class Server:
    def __init__(self, port):
        self.port = port
        self.server_socket = None
        self.running = True

    def transform_text(self, text):
        result = []

        for char in text:
            lower_char = char.lower()

            if lower_char in RUS_ALPHABET:
                index = RUS_ALPHABET.index(lower_char)

                # Сам символ в верхнем регистре
                result.append(lower_char.upper())

                # Следующие 5 символов (в нижнем регистре)
                for i in range(1, 6):
                    next_index = (index + i) % len(RUS_ALPHABET)
                    result.append(RUS_ALPHABET[next_index])
            else:
                # Не русские символы оставляем как есть
                result.append(char)

        return ''.join(result)

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("", self.port))
            self.server_socket.listen(5)
            print(f"[СЕРВЕР] Запущен на порту {self.port}")
            return True
        except OSError:
            print(f"[СЕРВЕР] Ошибка: порт {self.port} занят!")
            return False

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()

    def run(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"[СЕРВЕР] Подключен клиент: {addr}")

                # Запускаем обработку клиента в отдельном потоке
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.daemon = True
                client_thread.start()
            except:
                break

    def handle_client(self, client_socket, addr):
        try:
            while self.running:
                data = client_socket.recv(1024).decode("utf-8")

                if not data:
                    print(f"[СЕРВЕР] Клиент {addr} отключился")
                    break

                print(f"[СЕРВЕР] Получено от {addr}: {data}")

                # Проверка на команду выхода
                if data.lower() in ['exit', 'выход', 'quit']:
                    print(f"[СЕРВЕР] Клиент {addr} завершил сеанс")
                    client_socket.send("До свидания!".encode("utf-8"))
                    break

                # Проверка на наличие символа @
                if '@' in data:
                    parts = data.split('@', 1)
                    if len(parts) > 1:
                        before_at = parts[0]
                        text_to_transform = parts[1]
                        transformed = self.transform_text(text_to_transform)
                        response = f"{before_at}@{transformed}"
                        client_socket.send(response.encode("utf-8"))
                    else:
                        client_socket.send(data.encode("utf-8"))
                else:
                    # Если нет символа @, просто возвращаем исходное сообщение
                    client_socket.send(data.encode("utf-8"))

        except socket.error as e:
            print(f"[СЕРВЕР] Ошибка с клиентом {addr}: {e}")
        finally:
            client_socket.close()