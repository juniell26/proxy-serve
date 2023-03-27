def get_payload_size(request):
    content_length_header = b"Content-Length: "
    start_index = request.find(content_length_header)
    if start_index != -1:
        end_index = request.find(b"\r\n", start_index + len(content_length_header))
        if end_index != -1:
            content_length = int(request[start_index + len(content_length_header):end_index])
            return content_length
    return None

def get_response_payload_size(response):
    content_length_header = b"Content-Length: "
    start_index = response.find(content_length_header)
    if start_index != -1:
        end_index = response.find(b"\r\n", start_index + len(content_length_header))
        if end_index != -1:
            content_length = int(response[start_index + len(content_length_header):end_index])
            return content_length
    return None

def get_buffer_size(payload_size):
    buffer_sizes = {0: 1024, 1024: 4096, 4096: 8192, 8192: 16384, 16384: 32768, 32768: 65536}
    if payload_size is None:
        return 1024
    elif payload_size in buffer_sizes:
        return buffer_sizes[payload_size]
    else:
        return 65536
