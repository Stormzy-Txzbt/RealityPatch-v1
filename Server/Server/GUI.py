from PyQt6.QtWidgets import (
    QApplication, QMainWindow, 
    QTextEdit, QLineEdit, 
    QVBoxLayout, QWidget
)
from PyQt6.QtGui import QFont, QColor, QTextCharFormat
from PyQt6.QtCore import Qt, QTimer
import sys

class CyberChatGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RealityPatch [admin@localhost]")
        self.setGeometry(100, 100, 800, 600)
        
        # Deep hacker style
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 6px;
            }
            QTextEdit {
                background-color: #000000;
                border: none;
                color: #ffffff;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Courier New", 12))
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.returnPressed.connect(self.send_message)
        
        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def send_message(self):
        """Handle message sending"""
        message = self.input_field.text()
        if message:
            self.display_message("You", message)
            self.input_field.clear()
            
    def display_message(self, sender, message):
        """Add styled message to chat"""
        cursor = self.chat_display.textCursor()
        
        sender_fmt = QTextCharFormat()
        sender_fmt.setForeground(QColor("#ff5555"))
        sender_fmt.setFontWeight(75)
        
        msg_fmt = QTextCharFormat()
        msg_fmt.setForeground(QColor("#ffffff"))
        
        cursor.insertText(f"{sender}: ", sender_fmt)
        cursor.insertText(f"{message}\n", msg_fmt)
        
        self.chat_display.ensureCursorVisible()

def show_ascii_splash():
    splash = QTextEdit()
    splash.setReadOnly(True)
    splash.setStyleSheet("""
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        border: none;
    """)
    splash.setText("""
    [+] RealityPatch v1.0

      ______           _   _ _       _       _     
     |  __  \         | | (_) |     | |     | |    
     | |__) |___  __ _| |_ _| | __ _| |_ ___| |__  
     |  _  // _ \/ _` | __| | |/ _` | __/ __| '_ \ 
     | | \ \  __/ (_| | |_| | | (_| | || (__| | | |
     |_|  \_\___|\__,_|\__|_|_|\__,_|\__\___|_| |_|

        Terminal Chat Interface Initializing...
    """)
    splash.resize(720, 250)
    splash.setWindowTitle("RealityPatch Boot")
    splash.show()
    QTimer.singleShot(3000, splash.close)
    return splash

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    splash_screen = show_ascii_splash()
    window = CyberChatGUI()

    # Show main window after splash
    def show_main():
        window.show()

    QTimer.singleShot(3000, show_main)
    
    sys.exit(app.exec())
