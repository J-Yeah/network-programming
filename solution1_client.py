import socket
import pickle
import struct

# Client configuration — must match server HOST and PORT
HOST        = '127.0.0.1'
PORT        = 7777
BUFFER_SIZE = 4096


def recv_message(sock: socket.socket) -> object:
    # 1. read 4b
    header = b''
    while len(header) < 4:
        chunk = sock.recv(4 - len(header))
        if not chunk:
            raise ConnectionError("Disconnected")
        header += chunk

    # 2. read length
    length = struct.unpack('>I', header)[0]

    # 3. Unpickle
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Disconnected")
        data += chunk

    return pickle.loads(data)


def send_message(sock: socket.socket, obj: object) -> None:
    # 1. Pickle the object
    data = pickle.dumps(obj)
    # 2. Pack the length
    header = struct.pack('>I', len(data))
    # 3. Send the length header with data
    sock.sendall(header + data)


def parse_input(user_input: str) -> dict:
    tokens = user_input.strip().split()
    action = tokens[0]

    # ADD action
    if action == "ADD":
        if len(tokens) != 4:
            raise ValueError("ADD <name> <phone> <email>")

        return {
            "action": "ADD",
            "contact": {"name": tokens[1], "phone": tokens[2], "email": tokens[3]}
        }

    # SEARCH action
    elif action == "SEARCH":
        if len(tokens) != 2:
            raise ValueError("SEARCH <keyword>")

        return {
            "action": "SEARCH",
            "keyword": tokens[1]
        }

    # LIST action
    elif action == "LIST":
        return {
            "action": "LIST"
        }

    else:
        raise ValueError("Invalid command")


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print('Client has been assigned socket name', sock.getsockname())
    
    while True :
        try:
            user_input = input("> ")
            msg = parse_input(user_input)
           
            send_message(sock, msg)
            
            print(recv_message(sock))
  
    # exception handling    
    
        except ValueError as e:
            print("Input error:", e)
            continue
        
        except (BrokenPipeError, ConnectionResetError) as e:
            print("Disconnect error:", e)
            break
    
        except OSError as e:
            print("Network error:", e)
            break
            
        except Exception as e:
            print("Other errors:", e)
            break

    sock.close()