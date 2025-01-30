import socket
import time

# Create a server and a socket
server_ip = '127.0.0.1'

server_port = 5000

# Create a server socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def opening_connection():
    # Connect to server
    client_socket.connect((server_ip, server_port))
    print("Client: Connected to server")

    # Send SYN
    client_socket.send("SYN".encode())
    print("Client: SYN sent")

    # Receive SYN - ACK
    syn_ack_msg = client_socket.recv(1024).decode()
    if syn_ack_msg.upper() != "SYN-ACK":
        print("Client: SYN-ACK NOT received")
    else:
        print("Client: SYN-ACK received")

        # Send ACK
        client_socket.send("ACK".encode())
        print("Client: Sent ACK")

def closing_connection():
    # Send FIN-ACK
    client_socket.send("FIN-ACK".encode())
    print("Client: Sent FIN-ACK")

    # Receive ACK
    server_ack = client_socket.recv(1024).decode()
    if server_ack != "ACK":
        print("Incorrect message!")

    print(f"Client: ACK received!")

    server_fin_ack = client_socket.recv(1024).decode()
    if server_fin_ack != "FIN-ACK":
        print("Incorrect message!")
    print("Client: Received FIN-ACK")

    # Send ACK and stop the server
    client_socket.send("ACK".encode())
    print("Client: Sent ACK and stopping server...")

    client_socket.close()
    
def ui():
    opening_connection()
    while True:
        message = input("Enter message (Stop will end the connection): ")

        if message == "stop":
            client_socket.send("Stopping server".encode())
            print("Stopping the connection...")
            break

        client_socket.send(message.encode())

ui()