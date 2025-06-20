# Server/server.py
import socket
import threading
import sys
import signal
import atexit
from pyngrok import ngrok

class CyberChatServer:
    def __init__(self):
        self.port = int(input("[?] Enter port to bind the server: "))
        self.host = '0.0.0.0'
        self.server_socket = None
        self.clients = []  # list of client sockets
        self.client_names = {}  # mapping client socket to name
        self.running = False
        self.ngrok_tunnel = None

        # Cleanup handlers
        atexit.register(self.nuke)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)

    def handle_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        print(f"\n[!] Received shutdown signal ({signum})")
        self.nuke()
        sys.exit(0)

    def nuke(self):
        """Destroy all server artifacts"""
        print("[*] Nuking server...")
        self.stop_ngrok()
        self.stop_server()
        print("[+] System clean")

    def stop_ngrok(self):
        if self.ngrok_tunnel:
            ngrok.disconnect(self.ngrok_tunnel.public_url)
            self.ngrok_tunnel = None

    def start_ngrok(self):
        try:
            self.ngrok_tunnel = ngrok.connect(self.port, "tcp")
            return self.ngrok_tunnel.public_url
        except Exception as e:
            print(f"[!] Ngrok error: {e}")
            return None

    def setup_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"[+] Server socket bound to {self.host}:{self.port}")

    def broadcast(self, message, sender_socket=None):
        """Send message to all clients except the sender"""
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    # Remove dead client
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
        name = self.client_names.pop(client_socket, None)
        if name:
            print(f"[-] {name} disconnected")
            self.broadcast(f"[-] {name} left the chat", None)

    def handle_client(self, client_socket):
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
        except:
            pass
        finally:
            client_socket.close()
            self.remove_client(client_socket)

    def start(self):
        """Start the chat server"""
        try:
            self.setup_server_socket()
            public_url = self.start_ngrok()
            if public_url:
                print(f"\n[+] Server LIVE at {public_url}")
            print(f"[*] Server started on {self.host}:{self.port}")
            print("[*] Press Ctrl+C to shutdown\n")

            # Start a thread to accept clients
            accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
            accept_thread.start()
            accept_thread.join()  # Wait for the thread to finish (which is when server shuts down)

        except KeyboardInterrupt:
            print("\n[!] Manual shutdown initiated")
            self.nuke()
        except Exception as e:
            print(f"[!] Critical server error: {e}")
            self.nuke()
            sys.exit(1)

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"[+] New connection: {addr[0]}:{addr[1]}")
                self.clients.append(client_socket)
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True)
                client_thread.start()
            except OSError:
                # Server socket closed
                break

    def stop_server(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients = []
        self.client_names = {}

if __name__ == "__main__":
    server = CyberChatServer()
    server.start()