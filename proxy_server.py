import socket
import datetime

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to a specific IP address and port
server_socket.bind(('127.0.0.1', 8080))

# Listen for incoming connections
server_socket.listen(5)

# Loop indefinitely to handle incoming connections
while True:
    print('Waiting for a connection...')
    # Accept an incoming connection
    client_socket, client_address = server_socket.accept()
    print(f'Connected to {client_address}')

    # Receive the request from the client
    request = client_socket.recv(4096)

#segment1

    # Get additional information
    name = socket.getfqdn(client_socket.getpeername()[0])
    ip_address = client_socket.getpeername()[0]
    location = "N/A"  # Replace with your preferred method for determining location
    protocol = "HTTP"  # Replace with the actual protocol if known
    time = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    # Modify the request to include additional information
    modified_request = request.decode()
    modified_request += f"\r\nX-Client-Name: {name}\r\n"
    modified_request += f"X-Client-IP: {ip_address}\r\n"
    modified_request += f"X-Client-Location: {location}\r\n"
    modified_request += f"X-Client-Protocol: {protocol}\r\n"
    modified_request += f"X-Request-Time: {time}\r\n"
    modified_request = modified_request.encode()

    # Connect to the target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect(("192.168.106.247", 80))

    # Forward the modified request to the target server
    target_socket.send(modified_request)

    # Receive the response from the target server
    response = target_socket.recv(4096)

    # Forward the response back to the client
    client_socket.send(response)

    # Close the sockets
    client_socket.close()
    target_socket.close()
