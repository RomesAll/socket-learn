import socket
import threading
import os
import time

def main():
    HOST = '127.0.0.1'
    PORT = 65438
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        while True:
            data, addr = s.recvfrom(1024)
            print(f'Получено от {addr}: {data.decode()}')
            s.sendto('Сообщение получено UDP сервером'.encode(), addr)

if __name__ == "__main__":
    pid = os.getpid()
    print(f"PID текущего процесса: {pid}")
    main()