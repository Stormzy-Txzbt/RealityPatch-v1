from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QFont, QColor, QTextCharFormat
from PyQt6.QtCore import Qt, pyqtSignal, QObject


class Communicator(QObject):
    message_signal = pyqtSignal(str, str)


class CyberChatClientGUI(QMainWindow):
    def __init__(self, communicator):
        super().__init__()
        self.setWindowTitle("RealityPatch V1 - CyberChat")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #0d0d0d; color: #00ff00;")
        
        self.comm = communicator
        self.comm.message_signal.connect(self.display_message)
        self.init_ui()
    
    def init_ui(self):
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Courier New", 12))
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter message...")
        self.input_field.returnPressed.connect(self.handle_input)
        
        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_field)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def handle_input(self):
        message = self.input_field.text()
        if message:
            self.comm.message_signal.emit("You", message)
            self.input_field.clear()
    
    def display_message(self, sender, message):
        cursor = self.chat_display.textCursor()
        
        sender_fmt = QTextCharFormat()
        sender_fmt.setForeground(QColor("#00ffff"))
        sender_fmt.setFontWeight(75)
        
        msg_fmt = QTextCharFormat()
        msg_fmt.setForeground(QColor("#ffffff"))
        
        cursor.insertText(f"{sender}: ", sender_fmt)
        cursor.insertText(f"{message}\n", msg_fmt)
        self.chat_display.ensureCursorVisible()
