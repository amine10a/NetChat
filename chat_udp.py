import socket
import requests
from datetime import datetime

PORT = 5555
IP = "127.0.0.1"
ADDRESS = (IP, PORT)


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(ADDRESS)
            print("[*] Server is up and running at", ADDRESS)
        except OSError as e:
            print("Error binding to address:", e)
            return

        while True:
            try:
                data, client_address = s.recvfrom(1024)
                message = data.decode("UTF-8")
                print(f"Received message from {client_address} at {datetime.now()}:\n{message}")
                print("-----------------")
                
                response_message = input("Write your message: ")
                s.sendto(response_message.encode("UTF-8"), client_address)
            except Exception as e:
                print("Error:", e)


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while True:
            try:
                print("-----------------")
                message = input("Write your message: ")
                s.sendto(message.encode("UTF-8"), ADDRESS)
                
                data, server_address = s.recvfrom(1024)
                response_message = data.decode("UTF-8")
                print(f"Received message from {server_address} at {datetime.now()}:\n{response_message}")
            except Exception as e:
                print("Error:", e)


def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        if response.status_code == 200:
            data = response.json()
            return data.get('origin', None)
        print("Failed to fetch IP address")
        return None
    except requests.RequestException as e:
        print("Error fetching public IP address:", e)
        return None


def main():
    while True:
        print("You want to be the [1] Server or [2] Client?")
        try:
            choice = int(input("Choose (1 or 2): "))
            if choice == 1:
                run_server()
                break
            elif choice == 2:
                run_client()
                break
            else:
                print("Invalid choice. Please choose 1 for Server or 2 for Client.")
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")


if __name__ == "__main__":
    main()
