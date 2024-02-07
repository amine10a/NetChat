import socket
import requests
from datetime import datetime

port = 5555
ip = "127.0.0.1"  
address = (ip, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def server(address):
    try:
        s.bind(address)
        print("[*]:Server up")
    except OSError as e:
        print("Error binding to address:", e)
        return
    
    while True:
        try:
            Rdata, client_address = s.recvfrom(1024)
            data = Rdata.decode("UTF-8")
            print("Message from {} {}: \n {} ".format(client_address, str(datetime.now()), data))
            print("-----------------")
            msg = str(input("Write your message: "))
            print("-----------------")
            Sdata = msg.encode("UTF-8")
            s.sendto(Sdata, client_address)
        except Exception as e:
            print("Error:", e)

def client(address):
    while True:
        try:
            print("-----------------")
            msg = str(input("Write your message: "))
            print("-----------------")
            Sdata = msg.encode("UTF-8")
            s.sendto(Sdata, address)
            Rdata, server_address = s.recvfrom(1024)
            data = Rdata.decode("UTF-8")
            print("Message from {} {}: \n {} ".format(server_address, str(datetime.now()), data))
        except Exception as e:
            print("Error:", e)

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
