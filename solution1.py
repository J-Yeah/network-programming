import socket
import ssl
import json

# API configuration
HOST = 'timeapi.io'
PORT = 443                                        
PATH = '/api/v1/timezone/zone?timeZone=Asia/Seoul'

# HTTP request header
request_header = (
    "GET /api/v1/timezone/zone?timeZone=Asia/Seoul HTTP/1.1\r\n"
    "Host: timeapi.io\r\n"
    "Connection: close\r\n"
    "\r\n"
)


def chunk_parsing(body: str) -> str:
    i = 0
    result = ''

    while True:
        # read chunk size
        j = body.find('\r\n', i)
        if j == -1:
            raise ValueError("Invalid chunk format")
        chunk_size_hex = body[i:j]
        chunk_size = int(chunk_size_hex, 16)

        # if chunk size == 0, stop
        if chunk_size == 0:
            break

        # data start
        i = j + 2

        # read chunk data
        chunk_data = body[i:i + chunk_size]
        result += chunk_data

        # to next chunk
        i += chunk_size+2

    return result


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    context = ssl.create_default_context()
    sock = context.wrap_socket(sock, server_hostname=HOST)
    
    sock.connect((HOST, PORT))
    sock.sendall(request_header.encode())

    try:
        # recv reply
        reply = b''
        while True:
            more = sock.recv(4096)
            sock.settimeout(5)
            if not more :
                break
            reply += more
           
        # recv data decoding
        # if reply have char that cannot be decoded, they will be delete
        reply_str = reply.decode('utf-8', errors='ignore')
        
        # seperate header and body(json)
        header, body = reply_str.split('\r\n\r\n', 1)
    
        # header have to include 200 OK (If connected successfully)
        if "200" not in header:
            raise Exception("HTTP Error: " + header)
            
        # if body is chucked data, parse the chuck
        # Then loads json
        if 'Transfer-Encoding: chunked' in header:
            body = chunk_parsing(body)
        data = json.loads(body)
    
        # Extract and use data from JSON data by key
        print("local_time =", data['local_time'])
        print("timezone   =", data['timezone'])
        print("utc_time   =", data['utc_time'])

    except Exception as e:
        print("Other errors:", e)
        
    sock.close()