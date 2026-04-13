import threading
import time
from server import Server
from client import Client


class Main:
    # Настройки по умолчанию
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8001

    @staticmethod
    def run_server():
        server = Server(Main.DEFAULT_PORT)
        if server.start():
            server.run()

    @staticmethod
    def run_client():
        # Небольшая задержка для запуска сервера
        time.sleep(1)

        client = Client(Main.DEFAULT_HOST, Main.DEFAULT_PORT)
        if client.connect():
            print("\n=== КЛИЕНТ ЗАПУЩЕН ===")
            print("Введите сообщение (или 'exit' для выхода): ")
            client.run()

    @staticmethod
    def main():
        print("ЗАПУСК КЛИЕНТ-СЕРВЕРНОГО ПРИЛОЖЕНИЯ")
        print(f"Хост: {Main.DEFAULT_HOST}")
        print(f"Порт: {Main.DEFAULT_PORT}")

        # Запуск сервера в отдельном потоке
        server_thread = threading.Thread(target=Main.run_server, daemon=True)
        server_thread.start()

        # Запуск клиента в основном потоке
        Main.run_client()


if __name__ == "__main__":
    Main.main()