import socket
server_ip = '127.0.0.1'

server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

conn, addr = server_socket.accept()
print(f"Server listening on {server_ip}:{server_port}")

print(f"Connection accepted from {addr}")

def opening_connection():
    # Receive SYN
    syn_msg = conn.recv(1024).decode()
    if syn_msg == "SYN":
        print("Server: Received SYN from client")

    # Send ACK
    conn.send("SYN-ACK".encode())
    print("Server: Sent SYN-ACK to client")

    # Receive ACK
    ack_msg = conn.recv(1024).decode()
    if ack_msg == "ACK":
        print("Server: Received ACK from client. Handshake complete!")
        # server_socket.send("Completed!".encode())

def UI():
    opening_connection()
    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break

            if message == "stop":
                print(f"{message}")
                break

            print(f"Message received: {message}")

        except ConnectionError:
            print("Client disconnected")
            break

def closing_connection():
    # Send ACK after receiving FIN-ACK
    fin_msg = server_socket.recv(1024).decode()
    if fin_msg != "FIN-ACK":
        print("Server: No FIN-ACK received")

    print("Server: Received FIN-ACK from client")

    #Send ACK to client
    server_socket.send("ACK".encode())
    print("Server: Sending ACK to client")

    #Send FIN-ACK to client
    server_socket.send("FIN-ACK".encode())
    print("Server: Sending FIN-ACK to client")

    #Receive ACK from client
    ack_client = server_socket.recv(1024).decode()
    if ack_client == "ACK":
        print("Server: Received ACK from client")
        print(f"Client: {ack_client}")

        conn.close()
        server_socket.close()




