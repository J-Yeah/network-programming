import socket 

# Client configuration — must match server HOST and PORT
HOST        = '127.0.0.1'   # Server address
PORT        = 12345          # Server UDP port
BUFFER_SIZE = 1024           # Max datagram size
TIMEOUT_SEC = 5.0            # Seconds to wait for reply


# TODO: Write the code from here.

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # setting timeout
    sock.settimeout(TIMEOUT_SEC)

    try :
        while True :
            message = input("client sends: ").encode()
            #
            if len(message) >= BUFFER_SIZE:
                print("Warning: packet may be truncated")
            else :
                break
        
        # send data to server
        sock.sendto(message, (HOST,PORT))
        
        # recv response from server
        data, addr = sock.recvfrom(BUFFER_SIZE)
        # if reply have char that cannot be decoded, they will be delete
        print(data.decode('utf-8', errors='replace'))

    except socket.timeout:
        print("Timeout")

    except ValueError as e:
        print("Input error:", e)

    except OSError as e:
        print("Network error:", e)

    except Exception as e:
        print("Other errors:", e)
        
    sock.close()