import socket

# Client configuration — must match server HOST and PORT
HOST         = '127.0.0.1'
PORT         = 9999
BUFFER_SIZE  = 1024
MAX_ATTEMPTS = 3   # Must match server's limit


def get_integer_answer(attempt: int) -> str:
    # implement input validation
    while True :
        try :
            text = int(input(f"Attempt {attempt}. Try: "))
            break
        except :
            print("Please input valid integer.")
            continue
    return str(text)

    
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print('Client has been assigned socket name', sock.getsockname())
    
    try:
        while True :
            msg = input("press start: ").encode()
            if len(msg) >= BUFFER_SIZE :
                print("Too much data")
                continue
            sock.send(msg)
            reply = sock.recv(BUFFER_SIZE)
            
            # if reply have char that cannot be decoded, they will be delete
            reply = reply.decode('utf-8', errors='ignore')
            print(reply)
            
            # if quiz received, exit the loop and game start
            if "What is" in reply :
                break

        # 3 attempts
        for i in range(MAX_ATTEMPTS): 
            ans = get_integer_answer(i+1).encode()
            sock.send(ans)
            reply = sock.recv(BUFFER_SIZE)
            reply = reply.decode('utf-8', errors='ignore')
            print(reply)

            # game end and exit the loop immediately
            if "Game over" in reply or "You win" in reply :
                break

    
    # exception handling

    except ValueError as e:
        print("Input error:", e)

    except OSError as e:
        print("Network error:", e)

    except Exception as e:
        print("Other errors:", e)
    
    sock.close()