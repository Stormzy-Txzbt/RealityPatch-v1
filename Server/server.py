import sys
import signal
import atexit
from network import NetworkManager

class CyberChatServer:
    def __init__(self):
        port = int(input("[?] Enter port to bind the server: "))
        self.network = NetworkManager(port)
        self.clients = set()

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
        
        # Properly close all client connections
        for client in self.clients:
            try:
                client.close()
            except Exception as e:
                print(f"[!] Error closing client: {e}")
        self.clients.clear()
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
                
        except KeyboardInterrupt:
            print("\n[!] Manual shutdown initiated")
            self.nuke()
        except Exception as e:
            print(f"[!] Critical server error: {e}")
            self.nuke()
            sys.exit(1)

if __name__ == "__main__":
    server = CyberChatServer()
    server.start()