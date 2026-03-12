from PyQt6.QtWidgets import QLineEdit

class ClickableLineEdit(QLineEdit):
    from PyQt6.QtCore import pyqtSignal
    clicked = pyqtSignal()
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)