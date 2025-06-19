import subprocess
import sys

REQUIREMENTS = [
    'PyQt6',
]

def install_dependencies():
    print("[*] Installing dependencies...")
    for pkg in REQUIREMENTS:
        print(f" -> Installing {pkg}")
        subprocess.call([sys.executable, "-m", "pip", "install", pkg])

if __name__ == "__main__":
    install_dependencies()
    print("[+] Done. Run 'python client.py' to launch CyberChat.")
