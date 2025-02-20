import sys
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog, 
    QMainWindow, 
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
)
from SettingsLoader import *
OS = ""
DFPS = ""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam Artwork Manger")

        label = QLabel("Test")
        button = QPushButton("Press Me!")
        button.clicked.connect(buttonclicked)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.minimumSize()

class setupWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        DPS = SUOS()
        self.setWindowTitle("S.A.M Setup")
        labelOne = QLabel("The Path to steam")
        labelOne.font().setPointSize(20)
        TextBox = QLineEdit()
        TextBox.setText(DPS)
        layoutt = QVBoxLayout()
        layoutt.addWidget(labelOne)
        layoutt.addWidget(TextBox)
        container = QWidget()
        container.setLayout(layoutt)

        self.setCentralWidget(container)

        self.minimumSize()
     
def SUOS():
    if sys.platform == "win32":
        OS = "windows"
        DFPS = configL["DefaultSteamPaths"]["pathtosteamwin"]
    if sys.platform == "darwin":
        OS = "MacOS"
        DFPS = configL["DefaultSteamPaths"]["pathtosteammac"]
    if sys.platform == "linux" or sys.platform == "linux2":
        OS = "Linux"
        DFPS = configL["DefaultSteamPaths"]["pathtosteamlinux"]
    print("OS",OS,"DFPS",DFPS)
    return DFPS

def buttonclicked(self):
        print("Clicked!",)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    configLoader()
    SUOS()
    print("Setup mode",configL["AppSettings"]["setupmode"])
    if configL["AppSettings"]["setupmode"] == "True":
        SAMSUPW = setupWindows()
        SAMSUPW.show()
    else:
        SAMwindowMain = MainWindow()
        SAMwindowMain.show()
    
    app.exec()
