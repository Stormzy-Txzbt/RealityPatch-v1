import os
import sys
import subprocess
from pathlib import Path
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

REQUIREMENTS = [
    "pyngrok>=6.0.0",
    "colorama>=0.4.0",
    "PyQt6>=6.4.0"
]

def run_command(cmd):
    try:
        subprocess.check_call(cmd, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_dependencies():
    print(Fore.CYAN + "[*] Installing Python dependencies...\n")
    for package in REQUIREMENTS:
        print(Fore.YELLOW + f"  ├─ Installing {package}...")
        if run_command(f"{sys.executable} -m pip install {package}"):
            print(Fore.GREEN + f"  │   ✔ {package} installed.")
        else:
            print(Fore.RED + f"  │   ✘ Failed to install {package}.\n")

def setup_ngrok():
    print(Fore.CYAN + "\n[*] Checking ngrok setup...")

    if not shutil.which("ngrok"):
        print(Fore.RED + "  ✘ ngrok not found on this system.")
        print(Fore.YELLOW + "  → Download it from: https://ngrok.com/download")
        print("  → Unzip and move it to a directory in your PATH (or place it beside this script).")
    else:
        print(Fore.GREEN + "  ✔ ngrok is installed.")

    print(Fore.CYAN + "\n[*] Do you have your ngrok auth token?")
    answer = input(Fore.YELLOW + "  → If not, get it at https://dashboard.ngrok.com/get-started/your-authtoken\n  → Press Enter to continue once you have it...")

def setup_firewall():
    print(Fore.CYAN + "\n[*] Configuring firewall (if needed)...")
    platform = sys.platform

    if platform.startswith("linux"):
        print(Fore.YELLOW + "  ├─ Allowing TCP port 5000 via ufw...")
        run_command("sudo ufw allow 5000/tcp")
    elif platform == "darwin":
        print(Fore.YELLOW + "  ├─ macOS detected. Add port manually if needed.")
    elif platform == "win32":
        print(Fore.YELLOW + "  ├─ Windows detected. Skipping firewall auto-config.")
    else:
        print(Fore.RED + "  ├─ Unknown OS. Skipping firewall config.")

def summary():
    print(Fore.MAGENTA + "\n[+] Setup complete.")
    print(Fore.GREEN + "[*] Run with: python server.py")
    print(Fore.CYAN + "[*] You'll be prompted to enter your ngrok auth token at runtime if it's not already set.")

if __name__ == "__main__":
    import shutil
    install_dependencies()
    setup_ngrok()
    setup_firewall()
    summary()
