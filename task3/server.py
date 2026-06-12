from base import BaseTCPSocket
import socket, threading


class TCPServer(BaseTCPSocket):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.clients: list[socket.socket] = []
        self.threads: list[threading.Thread] = []

    def start(self):
        self._create_socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.is_running = True
        print(f"Сервер запущен на {self.host}:{self.port}")
        while self.is_running:
            client_socket: socket.socket
            address: tuple[str, str]
            client_socket, address = self.socket.accept()
            print(f"Новое подключение: {address}")
            thread = threading.Thread(
                target=self._handle_client, args=(client_socket, address)
            )
            thread.start()
            self.threads.append(thread)
            self.clients.append(client_socket)

    def stop(self):
        self.is_running = False
        if self.socket:
            self.socket.close()
        for client in self.clients:
            client.close()
        for thread in self.threads:
            thread.join(timeout=1)
        print(f"Сервер {self.host}:{self.port} остановлен")

    def _handle_client(self, client_socket: socket.socket, address: tuple[str, str]):
        """Обработка одного клиента в разных потоках"""
        try:
            client_socket.sendall("Привет от сервера".encode())
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Получено от {address}: {data.decode()}")
                client_socket.sendall(data)
        except (ConnectionResetError, BrokenPipeError):
            print(f"Клиент {address} разорвал соединение")
        finally:
            client_socket.close()
            self.clients.remove(client_socket)
            print(f"Клиент {address} отключен")

    def broadcast(self, message):
        """Отправляет сообщение всем подключённым клиентам."""
        for client in self.clients:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                client.close()
                self.clients.remove(client)
