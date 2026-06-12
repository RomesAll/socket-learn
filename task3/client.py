from base import BaseTCPSocket
import socket, threading


class TCPClient(BaseTCPSocket):
    def __init__(self, host='127.0.0.1', port=9999):
        super().__init__(host, port)
        self.connected = False

    def start(self):
        self._create_socket()
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f'Подключено к серверу {self.host}:{self.port}')
        except ConnectionRefusedError:
            print('Ошибка сервер не запущен')
            self.connected = False

    def stop(self):
        self.connected = False
        if self.socket:
            self.socket.close()
        print('Клиент отключен')

    def send(self, message):
        """Отправить сообщение серверу"""
        if not self.connected:
            raise RuntimeError('Клиент не подключен')
        self.socket.sendall(message.encode())

    def receive(self, buffer_size=1024):
        """Получает данные от сервера (блокирующий вызов)"""
        if not self.connected:
            raise RuntimeError('Клиент не подключен')
        return self.socket.recv(buffer_size).decode()

    def receive_until_close(self, callback=None):
        """Бесконечно читает данные от сервера (для отдельного потока)."""
        try:
            while self.connected:
                data = self.socket.recv(1024)
                if not data:
                    break
                if callback:
                    callback(data.decode('utf-8'))
                else:
                    print(f"Получено: {data.decode('utf-8')}")
        except (ConnectionResetError, OSError):
            pass
        finally:
            self.stop()

if __name__ == "__main__":
    client = TCPClient()
    client.start()

    # Получаем приветствие
    welcome = client.receive()
    print(f"Сервер: {welcome}")

    # Отправляем сообщение и получаем эхо
    client.send("Привет из ООП клиента!")
    response = client.receive()
    print(f"Эхо: {response}")

    client.stop()