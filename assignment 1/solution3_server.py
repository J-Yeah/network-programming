import socket
import random

# Server configuration
HOST         = '127.0.0.1'
PORT         = 9999
BUFFER_SIZE  = 1024
MAX_ATTEMPTS = 3


def play_game(conn: socket.socket, addr: tuple) -> None:
    # implement play_game 

    # if recv 'start' msg, game start
    while True:
            message = conn.recv(BUFFER_SIZE)
            msg = message.decode('utf-8', errors='ignore')
            if msg != "start" :
                conn.sendall(b"Error 400: Bad Request. Send 'start' to play.")
            else :
                break

    # creat random x and y
    ran_a = random.randint(1,20)
    ran_b = random.randint(1,20)

    # send quiz
    text = f"What is {ran_a} + {ran_b}?".encode()
    conn.sendall(text)
    
    ans = ran_a + ran_b
    cnt = 0
    
    while True :
        recvans = conn.recv(BUFFER_SIZE)

        # if recv answer have char that cannot be decoded, they will be delete
        recvans = int(recvans.decode('utf-8', errors='ignore'))

        
        # if correct, send msg and game end
        if recvans == ans :
            conn.sendall(b"Correct! You win.")
            conn.close()
            break
        else :
            # if recv wrong answer
            cnt += 1

            # if recv wrong answer more than max attempts, game over
            if cnt >= MAX_ATTEMPTS :
                text = f"Game Over. Out of attempts. The correct answer was {ans}.".encode()
                conn.sendall(text)
                conn.close()
                print('Reply sent, socket closed')
                break
            else :
                conn.sendall(b"Incorrect. Try again!")



if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    
    while True:
        try:
            print('Waiting to accept a new connection')
            # 3-way handshake
            conn, addr = sock.accept()
            print('We have accepted a connection from', addr)
            print('Socket name:', conn.getsockname())
            print('Socket peer:', conn.getpeername())

            # game start
            play_game(conn, addr)

        
        # exception handling
        
        except (BrokenPipeError, ConnectionResetError) as e:
            print("Disconnect error:", e)
            conn.close()
            continue
            
        except ValueError as e:
            print("Input error:", e)
            conn.close()
            continue

        except OSError as e:
            print("Network error:", e)
            conn.close()
            continue
        
        except Exception as e:
            print("Other errors:", e)
            conn.close()
            break
            
    sock.close()