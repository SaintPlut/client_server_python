import threading
import time
from server import Server
from client import Client


class Main:
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8888

    @staticmethod
    def print_usage():
        print("Использование:")
        print("  python main.py server     - Запустить сервер")
        print("  python main.py client     - Запустить клиента")
        print("  python main.py both       - Запустить и сервер, и клиента")
        print("\nНастройки по умолчанию:")
        print(f"  Хост: {Main.DEFAULT_HOST}")
        print(f"  Порт: {Main.DEFAULT_PORT}")

    @staticmethod
    def run_server():
        server = Server(Main.DEFAULT_PORT)
        server.start()

    @staticmethod
    def run_client():
        client = Client(Main.DEFAULT_HOST, Main.DEFAULT_PORT)
        if client.connect():
            client.run()

    @staticmethod
    def run_both():
        server_thread = threading.Thread(target=Main.run_server, daemon=True)
        server_thread.start()
        time.sleep(1)
        Main.run_client()

    @staticmethod
    def main():
        import sys
        if len(sys.argv) < 2:
            Main.print_usage()
            sys.exit(1)

        mode = sys.argv[1].lower()

        if mode == "server":
            Main.run_server()
        elif mode == "client":
            Main.run_client()
        elif mode == "both":
            Main.run_both()
        else:
            print(f"Ошибка: неизвестный режим '{mode}'")
            Main.print_usage()
            sys.exit(1)


if __name__ == "__main__":
    Main.main()