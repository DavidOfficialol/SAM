from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class twobythreeWCImage(QtWidgets.QWidget):
    """
    A widget that displays a 2 by 3 image with a label on the bottom.
    (600x900 Steam image)
    If the image is not set, it will display the caption on a gray backgroud.
    """
    def __init__(self, parent=None, imageP="", caption=""):
        
        super().__init__(parent)
        self.label = QtWidgets.QLabel()
        Image = QtGui.QPixmap(imageP)
        if Image.isNull():
            self.label.setText(caption)
            self.label.setStyleSheet("background-color: gray; color: white;")
        else:
            self.label.setPixmap(Image)
            self.label.setScaledContents(True)
            self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.label.setStyleSheet("background-color: black;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(Qt.RichText)   
        
    