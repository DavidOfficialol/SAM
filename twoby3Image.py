
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QSizePolicy, QPushButton

class twobythreeWCImage(QWidget):
    """
    A widget that displays a 2 by 3 image with a label on the bottom.
    (600x900 Steam image)
    If the image is not set, it will display the caption on a gray backgroud.
    """
    def __init__(self, imageP: str, caption: str ,h: int , w: int,Call: object, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.label = QPushButton()
        self.label.clicked.connect(Call)
        Image = QPixmap(imageP)
        if Image.isNull():
            self.label.setText(caption)
            self.label.setStyleSheet("background-color: gray; color: white;")
        else:
            Image = Image.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setIcon(Image)
            self.label.setIconSize(Image.size())
            self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.label.setStyleSheet("background-color: transparent;")
        self.label.setMaximumSize(w, h)
        self.captionla = QLabel()
        self.captionla.setText(caption)
        self.captionla.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(self.captionla)
        self.setLayout(layout)

    