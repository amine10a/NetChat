import socket
import requests
from datetime import datetime

port = 5555
ip = "192.168.0.157"  # my ip if I need to be the server
address = (ip, port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server(address):
    try:
        s.bind(address)
        s.listen(1)  # Listen for incoming connections
        print("[*]: Server up and listening")
        conn, client_address = s.accept()
        with conn:
            print("Connected by", client_address)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Message from {} {}: \n {} ".format(client_address, str(datetime.now()), data.decode("utf-8")))
                print("-----------------")
                msg = input("Write your message: ")
                print("-----------------")
                conn.sendall(msg.encode("utf-8"))
    except OSError as e:
        print("Error binding to address:", e)
        return
    except Exception as e:
        print("Error:", e)

def client(address):
    try:
        s.connect(address)
        print("[*]: Connected to server")
        while True:
            print("-----------------")
            msg = input("Write your message: ")
            print("-----------------")
            s.sendall(msg.encode("utf-8"))
            data = s.recv(1024)
            print("Message from server {}: \n {} ".format(str(datetime.now()), data.decode("utf-8")))
    except Exception as e:
        print("Error:", e)
    finally:
        s.close()

def get_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            return str(data['origin'])
        else:
            return "Failed to fetch IP address"
    except Exception as e:
        print("Error:", e)
        return None

def main():
    c = 0
    while c < 1 or c > 2:
        print("You want to be the [1]Server or [2]Client")
        c = int(input("choose : "))

    if c == 1:
        #ip = get_ip()
        address = (ip, port)
        server(address)
    elif c == 2:
        address = (ip, port)
        client(address)

main()
