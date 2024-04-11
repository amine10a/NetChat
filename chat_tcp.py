import socket
import requests
from datetime import datetime


def server(address):
    # Use context manager to handle socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(address)
            s.listen(1)  # Start listening for connections
            print(f"[*] Server is up and listening at {address}")
            
            # Accept connection from a client
            conn, client_address = s.accept()
            print(f"[*] Connection established with {client_address}")
            
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print(f"[*] Connection with {client_address} closed.")
                        break
                    print(f"[*] Received message from {client_address} at {datetime.now()}:\n{data.decode('utf-8')}")
                    print("-----------------")
                    
                    response = input("Write your response: ")
                    print("-----------------")
                    conn.sendall(response.encode("utf-8"))
        except Exception as e:
            print(f"[*] Server error: {e}")


def client(address):
    # Use context manager to handle socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(address)
            print(f"[*] Connected to server at {address}")
            
            while True:
                print("-----------------")
                message = input("Write your message: ")
                print("-----------------")
                
                s.sendall(message.encode("utf-8"))
                data = s.recv(1024)
                print(f"[*] Received response from server at {datetime.now()}:\n{data.decode('utf-8')}")
        except Exception as e:
            print(f"[*] Client error: {e}")


def main():
    port = 5555
    ip = "127.0.0.1"
    address = (ip, port)
    
    # Prompt user to choose whether to be a server or client
    choice = None
    while choice not in {1, 2}:
        try:
            choice = int(input("Choose [1] Server or [2] Client: "))
        except ValueError:
            print("Invalid choice. Please enter 1 for Server or 2 for Client.")
    
    # Execute based on user choice
    if choice == 1:
        server(address)
    elif choice == 2:
        client(address)


if __name__ == "__main__":
    main()
