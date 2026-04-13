import socket
import threading

RUS_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class Server:
    def __init__(self, port):
        self.port = port
        self.server_socket = None
        self.clients = []
        self.clients_lock = threading.Lock()

    def transform_text(self, text):
        """Преобразование текста: буква в верхнем регистре + 5 следующих в нижнем"""
        result = ""
        i = 0
        while i < len(text):
            char = text[i]
            if char.lower() in RUS_ALPHABET:
                idx = RUS_ALPHABET.index(char.lower())
                result += RUS_ALPHABET[idx].upper()
                for j in range(1, 6):
                    next_idx = (idx + j) % len(RUS_ALPHABET)
                    result += RUS_ALPHABET[next_idx]
            else:
                result += char
            i += 1
        return result

    def process_message(self, message):
        """Обработка всех символов @ в сообщении"""
        result = ""
        i = 0
        while i < len(message):
            if message[i] == '@' and i + 1 < len(message):
                result += '@'
                i += 1
                text_to_transform = ""
                while i < len(message) and message[i] != '@':
                    text_to_transform += message[i]
                    i += 1
                result += self.transform_text(text_to_transform)
            else:
                result += message[i]
                i += 1
        return result

    def send_to_all_clients(self, message):
        """Отправить сообщение ВСЕМ клиентам (включая отправителя)"""
        with self.clients_lock:
            disconnected = []
            for client in self.clients:
                try:
                    client['socket'].send(message.encode('utf-8'))
                except:
                    disconnected.append(client)

            for client in disconnected:
                self.clients.remove(client)

    def handle_client(self, client_socket, addr):
        """Обработка одного клиента в отдельном потоке"""
        print(f"Клиент подключен: {addr}")

        # Добавляем клиента в список
        with self.clients_lock:
            self.clients.append({'socket': client_socket, 'addr': addr})

        # Уведомляем всех о новом клиенте
        self.send_to_all_clients(f"[СИСТЕМА] Клиент {addr} подключился. Всего клиентов: {len(self.clients)}")

        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(f"Получено от {addr}: {data}")

                # Проверка на выход
                if data.lower() == 'exit':
                    client_socket.send("До свидания!".encode('utf-8'))
                    break

                # Обрабатываем сообщение (преобразуем все @)
                processed_message = self.process_message(data)

                # ОТПРАВЛЯЕМ ВСЕМ КЛИЕНТАМ ОДИНАКОВУЮ ИНФОРМАЦИЮ
                # Формируем сообщение для рассылки
                broadcast_message = f"[{addr}] {processed_message}"

                # Отправляем ВСЕМ клиентам (включая отправителя)
                self.send_to_all_clients(broadcast_message)

            except Exception as e:
                print(f"Ошибка: {e}")
                break

        # Удаляем клиента
        with self.clients_lock:
            self.clients = [c for c in self.clients if c['socket'] != client_socket]

        # Уведомляем всех об отключении
        self.send_to_all_clients(f"[СИСТЕМА] Клиент {addr} отключился. Осталось клиентов: {len(self.clients)}")

        print(f"Клиент отключен: {addr}")
        client_socket.close()

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('', self.port))
            self.server_socket.listen(5)
            print(f"Сервер запущен на порту {self.port}")
            print(f"Ожидание подключения клиентов...")

            while True:
                client_socket, addr = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.daemon = True
                thread.start()

        except OSError:
            print("Ошибка: порт занят!")
            return
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            if self.server_socket:
                self.server_socket.close()


if __name__ == "__main__":
    port = int(input("Введите порт сервера: "))
    server = Server(port)
    server.start()