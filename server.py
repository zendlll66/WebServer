from socket import *
def handle_request(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        if not filename.startswith('/'):
            raise IOError

        with open(filename[1:], 'rb') as f:
            outputdata = f.read()
        response_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        connectionSocket.send(response_header.encode())
        connectionSocket.sendall(outputdata)

    except IOError:
        response_header = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        error_message = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
        connectionSocket.send(response_header.encode())
        connectionSocket.send(error_message.encode())

    except Exception as e:
        response_header = "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n"
        error_message = "<html><head></head><body><h1>500 Internal Server Error</h1></body></html>\r\n"
        connectionSocket.send(response_header.encode())
        connectionSocket.send(error_message.encode())

    finally:
        connectionSocket.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverPort = 2222
    try:
        serverSocket.bind(('', serverPort))
        serverSocket.listen(1)
        print('server is ready!!!')

        while True:
            connectionSocket, addr = serverSocket.accept()
            handle_request(connectionSocket)

    except KeyboardInterrupt:
        print("\nServer shutting down...")
        serverSocket.close()
        print("Server closed.")

if __name__ == "__main__":
    main()