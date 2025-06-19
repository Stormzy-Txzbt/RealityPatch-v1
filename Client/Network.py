import socket
import threading


class NetworkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        self.socket.connect((self.host, self.port))
    
    def send(self, message):
        self.socket.sendall(message.encode())
    
    def receive_loop(self, callback):
        def loop():
            while True:
                try:
                    data = self.socket.recv(4096).decode()
                    if data:
                        callback("Server", data)
                except:
                    break
        
        thread = threading.Thread(target=loop, daemon=True)
        thread.start()
