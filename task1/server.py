import socket
import threading
import os
import time

def handle_client(conn, addr):
    """Обрабатывает соединение с клиентом."""
    print(f"Подключен клиент: {addr}")
    with conn:
        data = conn.recv(1024)
        if data:
            print('Сообщение от клиента ' + data.decode())
            conn.sendall('Привет от сервера'.encode())
    print(f'Клиент: {addr} отключен')

def main():
    HOST = '127.0.0.1'
    PORT = 65434
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    pid = os.getpid()
    print(f"PID текущего процесса: {pid}")
    main()