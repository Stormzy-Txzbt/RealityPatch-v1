import sys
import socket
import threading

# Try to load GUI
try:
    from Gui import CyberChatClientGUI, Communicator
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

# ======== Common Networking Setup ========
class ChatClient:
    def __init__(self, host, port):
        self.server_addr = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect(self.server_addr)
            print(f"[+] Connected to {self.server_addr[0]}:{self.server_addr[1]}")
        except Exception as e:
            print(f"[!] Failed to connect: {e}")
            sys.exit(1)

    def send(self, msg):
        try:
            self.socket.send(msg.encode())
        except:
            print("[-] Failed to send message.")

    def receive_loop(self, callback):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                callback(data)
            except:
                break

# ======== Terminal CLI Mode ========
def cli_mode(client):
    def handle_incoming(msg):
        print(msg)

    threading.Thread(target=client.receive_loop, args=(handle_incoming,), daemon=True).start()

    while True:
        try:
            msg = input("> ")
            if msg.lower() in ["exit", "quit"]:
                break
            client.send(msg)
        except KeyboardInterrupt:
            break

    print("[*] Disconnected.")
    client.socket.close()

# ======== Main Logic ========
if __name__ == "__main__":
    host = input("[?] Server address (e.g. 0.tcp.ngrok.io): ").strip()
    port = int(input("[?] Port (e.g. 12345): ").strip())

    client = ChatClient(host, port)
    client.connect()

    if GUI_AVAILABLE:
        print("[*] GUI mode detected. Launching CyberChat GUI...")
        app = Communicator(client)
        app.run()
    else:
        print("[*] GUI not available. Switching to CLI mode.")
        cli_mode(client)
