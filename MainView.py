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
Settingdic = {}
OS = ""
DFPS = ""
Setupdone = True
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
# Setup Windows
class setupWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        DPS = SUOS()
        self.setWindowTitle("S.A.M Setup")
        labelOne = QLabel("The Path to steam")
        labelOne.setAlignment(Qt.AlignCenter)
        labelTwo = QLabel("The path to your steam installaion")
        labelTwo.setAlignment(Qt.AlignCenter)
        LOF = labelOne.font()
        LOF.setPointSize(20)
        labelOne.setFont(LOF)
        self.TextBox = QLineEdit()
        self.TextBox.setText(DPS)
        layoutt = QVBoxLayout()
        layoutt.addWidget(labelOne)
        layoutt.addWidget(labelTwo)
        layoutt.addWidget(self.TextBox)
        container = QWidget()
        container.setLayout(layoutt)
        self.setMinimumSize(500,250)
        self.setBaseSize(650,500)
        self.setCentralWidget(container)
        self.TextBox.returnPressed.connect(self.Setuptextboxenter)
    # When the enter key is pressed in the textbox
    def Setuptextboxenter(self):
        print("Enter Pressed")
        print(self.TextBox.text())
        Settingdic["Pathtosteam"] = self.TextBox.text()
        print(Settingdic)
# When the enter key is pressed in the textbox

# Finds to OS that is being used 
def SUOS():
    if sys.platform == "win32":
        OS = "windows"
        Settingdic["OS"] = "Windows"
        DFPS = configL["DefaultSteamPaths"]["pathtosteamwin"]
    if sys.platform == "darwin":
        OS = "MacOS"
        Settingdic["OS"] = "MacOS"
        DFPS = configL["DefaultSteamPaths"]["pathtosteammac"]
    if sys.platform == "linux" or sys.platform == "linux2":
        OS = "Linux"
        Settingdic["OS"] = "Linux" 
        DFPS = configL["DefaultSteamPaths"]["pathtosteamlinux"]
    print("OS",OS,"DFPS",DFPS)
    return DFPS

def SDLoder():
    Settingdic["DarkMode"] = configL["AppSettings"]["DarkMode"]
    Settingdic["LocalImageRepostory"] = configL["AppSettings"]["LocalImageRepostory"]
    Settingdic["Pathtosteam"] = configL["Steam"]["Pathtosteam"]
    Settingdic["User"] = configL["Steam"]["User"]
    print(Settingdic)
    return Settingdic

def buttonclicked(self):
        print("Clicked!",)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    configLoader()
    SUOS()
    SDLoder()
    print("Setup mode",configL["AppSettings"]["setupmode"])
    if configL["AppSettings"]["setupmode"] == "True":
        Setupdone = False
        SAMSUPW = setupWindows()
        SAMSUPW.show()
    else:
        SAMwindowMain = MainWindow()
        SAMwindowMain.show()
    app.exec()
