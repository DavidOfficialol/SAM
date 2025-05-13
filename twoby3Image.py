
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QSizePolicy

class twobythreeWCImage(QWidget):
    """
    A widget that displays a 2 by 3 image with a label on the bottom.
    (600x900 Steam image)
    If the image is not set, it will display the caption on a gray backgroud.
    """
    def __init__(self, imageP: str, caption: str ,h: int , w: int, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.label = QLabel()
        Image = QPixmap(imageP)
        if Image.isNull():
            self.label.setText(caption)
            self.label.setStyleSheet("background-color: gray; color: white;")
        else:
            Image = Image.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(Image)
            self.label.hasScaledContents = True
            self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMaximumSize(w, h)
        self.captionla = QLabel()
        self.captionla.setText(caption)
        self.captionla.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        layout.addWidget(self.captionla)
        self.setLayout(layout)

    