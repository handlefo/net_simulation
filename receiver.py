import socket

def receive_file(file_path, host, port):
    chunk_size = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    with open(file_path, 'wb') as f:
        while True:
            data, addr = sock.recvfrom(chunk_size)
            if not data:
                break
            f.write(data)

    print('File received successfully')

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 12345
    file_path = 'received.jpg'
    receive_file(file_path, host, port)
