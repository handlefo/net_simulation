import socket

def send_file(file_path, host, port):
    chunk_size = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(file_path, 'rb') as f:
        data = f.read(chunk_size)
        while data:
            sock.sendto(data, (host, port))
            data = f.read(chunk_size)

    sock.sendto(b'', (host, port))  # Send an empty packet to indicate end of file

    print('File sent successfully')

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 12345
    file_path = 'example.jpg'
    send_file(file_path, host, port)
