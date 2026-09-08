import socket

# Server configuration
HOST        = '127.0.0.1'
PORT        = 12345
BUFFER_SIZE = 1024


def count_vowels(message: str) -> int:
    # implement vowel counting here
    cnt = 0
    for i in message :
        if i in "AEIOUaeiou":
            cnt += 1
    return cnt



if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    try:
        while True:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)

                # check abnormal data or too much request
                if not data or len(data) > BUFFER_SIZE:
                    raise ValueError("Invalid data")
                    
                # recv data decoding
                # if reply have char that cannot be decoded, they will be delete
                message = data.decode('utf-8', errors='replace')
                #print('The client at {} says {!r}'.format(addr, message))
                
                vowel = count_vowels(message)
                message = f"Vowel count: {vowel}"
                
                data = message.encode()
                sock.sendto(data, addr)
                
            except ValueError as e:
                print("Input error:", e)
                continue

            except OSError as e:
                print("Network error:", e)
                continue
                #but we wants udp server still running...
                
    except KeyboardInterrupt:
        print("Server shutting down...")

    sock.close()