import socket

def start_client(port):
    host = "localhost"

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Receive data from the server
    data = client_socket.recv(1024)

    # Print the received data
    print(data.decode())

    # Send a message to the server
    message = "Hello from the client"
    client_socket.sendall(message.encode())

    # Receive data from the server
    data = client_socket.recv(1024)

    # Print the received data
    print(data.decode())

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    start_client(8000)
