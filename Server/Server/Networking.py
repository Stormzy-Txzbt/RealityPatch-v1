networking.py

import socket
import threading

HOST = '0.0.0.0' PORT = 9999

class ChatServer: def init(self, host=HOST, port=PORT): self.host = host self.port = port self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) self.clients = [] self.client_names = {} self.running = False

def start(self):
    self.server.bind((self.host, self.port))
    self.server.listen(5)
    self.running = True
    print(f"[+] Server started on {self.host}:{self.port}")

    threading.Thread(target=self.accept_clients, daemon=True).start()

def accept_clients(self):
    while self.running:
        try:
            client_socket, addr = self.server.accept()
            print(f"[+] Connection from {addr}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
        except:
            break

def broadcast(self, message, sender_socket=None):
    for client in self.clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                if client in self.clients:
                    self.clients.remove(client)

def handle_client(self, client_socket):
    try:
        client_socket.send("Enter your name: ".encode())
        name = client_socket.recv(1024).decode().strip()
        self.client_names[client_socket] = name
        self.broadcast(f"[+] {name} joined the chat.", client_socket)

        while self.running:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            full_message = f"{name}: {message}"
            self.broadcast(full_message, client_socket)
    except:
        pass
    finally:
        name = self.client_names.get(client_socket, 'A user')
        print(f"[-] {name} disconnected.")
        self.broadcast(f"[-] {name} left the chat.", client_socket)
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        if client_socket in self.client_names:
            del self.client_names[client_socket]
        client_socket.close()

def stop(self):
    self.running = False
    for client in self.clients:
        try:
            client.send("Server is shutting down.".encode())
            client.close()
        except:
            pass
    self.clients.clear()
    self.client_names.clear()
    self.server.close()

