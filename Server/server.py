import os import sys import signal import atexit from network import NetworkManager

class CyberChatServer: def init(self): port = int(input("[?] Enter port to bind the server: ")) self.network = NetworkManager(port) self.clients = set()

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
    self.network.stop_ngrok()
    for client in self.clients:
        try:
            client.close()
        except:
            pass
    print("[+] System clean")

def start(self):
    """Start the chat server"""
    try:
        public_url = self.network.start_ngrok()
        print(f"\n[+] Server LIVE at {public_url}")
        print("[*] Press Ctrl+C to shutdown\n")

        while True:
            client, addr = self.network.accept_connection()
            self.clients.add(client)
            print(f"[+] New connection: {addr[0]}:{addr[1]}")

    except Exception as e:
        print(f"[!] Server error: {e}")
        self.nuke()

if name == "main": server = CyberChatServer() server.start()

