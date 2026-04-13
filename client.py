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
            print(f"Подключен к серверу {self.host}:{self.port}")
            return True
        except socket.error:
            print("Ошибка: не удалось подключиться к серверу")
            return False

    def receive_messages(self):
        while self.running:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                if response:
                    print(f"\n{response}")
                    print("> ", end="", flush=True)
                else:
                    break
            except:
                break

    def run(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

        print("\n" + "=" * 50)
        print("ЧАТ ЗАПУЩЕН")
        print("@ - преобразование текста")
        print("exit - выход")
        print("=" * 50)
        print("> ", end="", flush=True)

        while self.running:
            try:
                message = input()

                if message.lower() == 'exit':
                    self.client_socket.send('exit'.encode('utf-8'))
                    break

                if message:
                    self.client_socket.send(message.encode('utf-8'))

                print("> ", end="", flush=True)

            except KeyboardInterrupt:
                break

        self.running = False
        self.client_socket.close()
        print("Соединение закрыто")


if __name__ == "__main__":
    host = input("Введите IP-адрес сервера: ")
    port = int(input("Введите порт сервера: "))
    client = Client(host, port)
    if client.connect():
        client.run()