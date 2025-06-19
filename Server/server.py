import socket
import threading
import sys
import signal

HOST = '0.0.0.0'
PORT = 9999

clients = []
client_names = {}

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                if client in clients:
                    clients.remove(client)

def handle_client(client_socket):
    try:
        client_socket.send("Enter your name: ".encode())
        name = client_socket.recv(1024).decode().strip()
        client_names[client_socket] = name
        welcome = f"[+] {name} joined the chat."
        print(welcome)
        broadcast(welcome, client_socket)

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            full_message = f"{name}: {message}"
            print(full_message)
            broadcast(full_message, client_socket)
    except:
        pass
    finally:
        print(f"[-] {client_names.get(client_socket, 'A user')} disconnected.")
        broadcast(f"[-] {client_names.get(client_socket, 'A user')} left the chat.", client_socket)
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in client_names:
            del client_names[client_socket]
        client_socket.close()

def cleanup_and_exit(*args):
    print("\n[!] Server shutting down. Nuking all sessions.")
    for client in clients:
        try:
            client.send("Server is shutting down.".encode())
            client.close()
        except:
            pass
    clients.clear()
    client_names.clear()
    sys.exit(0)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Server started on {HOST}:{PORT}")

    signal.signal(signal.SIGINT, cleanup_and_exit)
    signal.signal(signal.SIGTERM, cleanup_and_exit)

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Connection from {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
