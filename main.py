import socket
import sys
import gzip
import segment1

# Set the default buffer size
DEFAULT_BUFFER_SIZE = 4096

# Set the address and port of the proxy server
proxy_address = '192.168.56.1'
proxy_port = 8080

# Set the address and port of the Apache server
apache_address = '192.168.254.147'
apache_port = 80

# Create a TCP/IP socket for the proxy server
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the proxy address and port
proxy_socket.bind((proxy_address, proxy_port))

# Listen for incoming connections
proxy_socket.listen(5)

# Define a function to detect the size of the payload
def get_payload_size(request):
    
    # Parse the request to get the content length
    content_length = None
    lines = request.split(b"\r\n")
    for line in lines:
        if line.startswith(b"Content-Length:"):
            content_length = int(line.split(b":")[1].strip())
            break
    if content_length is None:
        return None
    
    # Return the payload size in bytes
    return content_length

# Define a function to get the buffer size based on the payload size
def get_buffer_size(payload_size):
    if payload_size is None:
        return DEFAULT_BUFFER_SIZE
    elif payload_size > 100000000:  # 100 MB
        return 65536
    elif payload_size > 10000000:  # 10 MB
        return 16384
    else:
        return DEFAULT_BUFFER_SIZE

# Loop forever, accepting incoming connections
while True:
    # Accept a connection
    client_socket, client_address = proxy_socket.accept()
    print('A client has connected')

    # Print the client IP address
    print("Client connected from:", client_address[0])

    # Read the incoming request from the client
    request = client_socket.recv(DEFAULT_BUFFER_SIZE)

    # Determine the size of the payload
    payload_size = get_payload_size(request)

    # Get the buffer size based on the payload size
    buffer_size = get_buffer_size(payload_size)

    # Create a TCP/IP socket for the Apache server
    apache_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Forward the request to the Apache server
        apache_socket.connect((apache_address, apache_port))
        apache_socket.sendall(request)
        print(f'Forwarding the request to {apache_address}:{apache_port}')

        # Receive the response from the Apache server
        response = b""
        while True:
            data = apache_socket.recv(buffer_size)
            if not data:
                break
            response += data

        # Set the response headers
        response_headers = [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Encoding", "gzip")
        ]

        # Compress the response data
        compressed_data = gzip.compress(response)

        # Send the response headers
        for header in response_headers:
            header_str = "{}: {}\r\n".format(header[0], header[1])
            client_socket.sendall(header_str.encode("utf-8"))

        # Send the compressed response data
        client_socket.sendall(compressed_data)

        # Send the response back to the client
        client_socket.sendall(response)
    except Exception as e:
        print(f"Error occurred while forwarding the request: {e}")
    finally:
        # Close the sockets
        apache_socket.close()
        client_socket.close
