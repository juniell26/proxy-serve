import requests
import sys

# Create a dictionary to keep track of IP addresses and their request count
ip_requests = {}

def process_data(data):
    # Get the IP address of the client making the request
    client_ip = requests.remote_addr

    # Check if the client has made too many requests in a short amount of time
    if client_ip in ip_requests and ip_requests[client_ip] > 100:
        print("Request bombing detected from", client_ip, ". Shutting down the system.")
        sys.exit()

    # Increment the request count for the client's IP address
    if client_ip in ip_requests:
        ip_requests[client_ip] += 1
    else:
        ip_requests[client_ip] = 1

    # Process the data received from the previous segment
    processed_data = data + " from segment 4"

    # Send the processed data to the Apache server and receive a response
    url = "http://localhost:8080"  # Replace with the URL of your Apache server
    headers = {"Content-Type": "text/plain"}
    response = requests.post(url, data=processed_data, headers=headers)

    # Print the response received from the Apache server
    print("Response from Apache server:", response.text)

    return processed_data
