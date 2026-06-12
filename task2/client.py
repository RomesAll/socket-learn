import socket, threading

def main():
    HOST = '127.0.0.1'
    PORT = 65438
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message = 'Hello, world'.encode()
        s.sendto(message, (HOST, PORT))
        s.settimeout(2.0)
        try:
            data, addr = s.recvfrom(1024)
            print(data.decode(), addr)
        except socket.timeout:
            print('no')

if __name__ == '__main__':
    main()