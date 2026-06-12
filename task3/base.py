import socket
from abc import ABC, abstractmethod

class BaseTCPSocket(ABC):
    """Абстрактный базовый класс для сокетов."""

    def __init__(self, host='127.0.0.1', port=9999):
        self.host = host
        self.port = port
        self.socket = None
        self.is_running = False

    @abstractmethod
    def start(self):
        """Запуск сервера или клиента"""
        pass

    @abstractmethod
    def stop(self):
        """Остановка сервера или клиента"""
        pass

    def _create_socket(self):
        """Создание TCP-сокета"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)