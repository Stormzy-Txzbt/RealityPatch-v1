# Server/network.py
import socket
import threading
from pyngrok import ngrok

class NetworkManager:
    def __init__(self, port):
        self.port = port
        self.host = '0.0.0.0'
        self.server_socket = None
        self.clients = []
        self.client_names = {}
        self.running = False
        self.ngrok_tunnel = None

    def start_ngrok(self):
        """Start ngrok tunnel and return public URL"""
        self.ngrok_tunnel = ngrok.connect(self.port, "tcp")
        return self.ngrok_tunnel.public_url

    def stop_ngrok(self):
        """Stop ngrok tunnel if active"""
        if self.ngrok_tunnel:
            ngrok.disconnect(self.ngrok_tunnel.public_url)

    def setup_server(self):
        """Initialize server socket"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"[*] Server socket bound to {self.host}:{self.port}")

    def accept_connection(self):
        """Accept incoming client connections"""
        if not self.server_socket:
            self.setup_server()
            
        client_socket, addr = self.server_socket.accept()
        print(f"[+] New connection: {addr[0]}:{addr[1]}")
        return client_socket, addr

    def broadcast(self, message, sender_socket=None):
        """Send message to all clients except sender"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    self.remove_client(client)

    def add_client(self, client_socket):
        """Add new client and start handler thread"""
        self.clients.append(client_socket)
        threading.Thread(
            target=self.handle_client, 
            args=(client_socket,),
            daemon=True
        ).start()

    def handle_client(self, client_socket):
        """Manage individual client communication"""
        try:
            client_socket.send("Enter your name: ".encode())
            name = client_socket.recv(1024).decode().strip()
            self.client_names[client_socket] = name
            self.broadcast(f"[+] {name} joined the chat", client_socket)

            while self.running:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                full_message = f"{name}: {message}"
                self.broadcast(full_message, client_socket)
        except Exception as e:
            print(f"[-] Client error: {e}")
        finally:
            self.remove_client(client_socket)

    def remove_client(self, client_socket):
        """Clean up disconnected clients"""
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            
        name = self.client_names.pop(client_socket, 'Unknown')
        print(f"[-] {name} disconnected")
        self.broadcast(f"[-] {name} left the chat", client_socket)
        client_socket.close()

    def shutdown(self):
        """Graceful server shutdown"""
        self.running = False
        self.stop_ngrok()
        
        # Close all client connections
        for client in self.clients:
            try:
                client.send("Server is shutting down".encode())
                client.close()
            except:
                pass
        
        # Close server socket
        if self.server_socket:
            self.server_socket.close()
        
        self.clients.clear()
        self.client_names.clear()