import socket, threading

def main():
    HOST = '127.0.0.1'
    PORT = 65434
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Подключено к серверу {HOST}:{PORT}")
        s.sendall('Hello, world'.encode())
        data = s.recv(1024).decode()
        print(data)

if __name__ == '__main__':
    main()