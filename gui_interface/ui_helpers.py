from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal

class ExtendedQLabel(QLabel):
    '''
    The extended Label support click
    '''
    def __init__(self, parent):
        QLabel.__init__(self, parent)

    clicked=pyqtSignal()
    def mouseReleaseEvent(self, ev):
        self.clicked.emit()


class Pop_Up(QDialog):
    
    def __init__(self, parent, message):
        super().__init__(parent)
        
        # Define the layout managers
        self.layout_manager = QVBoxLayout()
        
        # Define the different widgets
        self.text = QLabel(message)
        self.button = QPushButton("Ok")
        self.button.clicked.connect(self.accept)
        
        # Set up the window
        self.layout_manager.addWidget(self.text)
        self.layout_manager.addWidget(self.button)
        self.setWindowTitle("Error")
        self.setLayout(self.layout_manager)
        self.setModal(True)


class Connection_Error_Pop_Up(QDialog):
    
    def __init__(self, parent, message):
        super().__init__(parent)
        
        # Define layout managers
        self.layout_manager = QVBoxLayout()
        self.button_layout_manger = QHBoxLayout()
        
        # Define the different widgets
        self.text = QLabel(message)
        self.accept_button = QPushButton("Retry")
        self.reject_button = QPushButton("Exit")
        
        # Connect the buttons to their handles
        self.accept_button.clicked.connect(self.accept)
        self.reject_button.clicked.connect(self.reject)
        
        # Add widgets to their layout managers
        self.button_layout_manger.addWidget(self.accept_button)
        self.button_layout_manger.addWidget(self.reject_button)
        self.layout_manager.addWidget(self.text)
        self.layout_manager.addLayout(self.button_layout_manger)
        
        # Set up the window
        self.setWindowTitle("Error")
        self.setLayout(self.layout_manager)
        self.setModal(True)
        
    def accept(self):
        self.parent.connection_worker.start()
        self.hide()
        
    def reject(self):
        exit(0)
