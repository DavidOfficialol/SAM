from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

class twobythreeWCImage(QtWidgets.QWidget):
    """
    A widget that displays a 2 by 3 image with a label on the bottom.
    (600x900 Steam image)
    If the image is not set, it will display the caption on a gray backgroud.
    """
    def __init__(self, parent=None):
        super().__init__(parent)