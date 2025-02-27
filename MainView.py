import sys
import vdf
from pathlib import Path, PurePath 
home = Path.home()
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog, 
    QMessageBox,
    QMainWindow, 
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
)
from SettingsLoader import *
Settingdic = {}
OS = ""
DFPS = ""
Setupdone = True
ASUsers = {}
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steam Artwork Manger")

        label = QLabel("Test")
        layout = QVBoxLayout()
        layout.addWidget(label)
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        self.minimumSize()
# Setup Windows
class setupWindows(QMainWindow):
    Index = 0
    def __init__(self):
        super().__init__()
        DPS = SUOS()
        self.setWindowTitle("S.A.M Setup")
        self.labelOne = QLabel("The Path to steam")
        self.labelOne.setAlignment(Qt.AlignCenter)
        self.labelTwo = QLabel("The path to your steam installaion. Please make sure you include to full path to the steam folder eg. " + DPS)
        self.labelTwo.setAlignment(Qt.AlignCenter)
        LOF = self.labelOne.font()
        LOF.setPointSize(20)
        self.labelOne.setFont(LOF)
        self.TextBox = QLineEdit()
        self.TextBox.setText(DPS)
        self.but = QPushButton("Next")
        layoutt = QVBoxLayout()
        Textlayout = QHBoxLayout()
        Textlayout.addWidget(self.TextBox)
        Textlayout.addWidget(self.but)
        Textlayout.setSpacing(10)
        layoutt.addWidget(self.labelOne)
        layoutt.addWidget(self.labelTwo)
        layoutt.addLayout(Textlayout)
        container = QWidget()
        container.setLayout(layoutt)
        self.setMinimumSize(500,250)
        self.setBaseSize(650,500)
        self.setCentralWidget(container)
        self.TextBox.returnPressed.connect(self.Setuptextboxenter)
        self.but.clicked.connect(self.nextbutton)
    def nextbutton(self):
        print("Next Button Clicked")
        if self.Index == 3:
            print("setup done")
            return
        self.Setuptextboxenter()
    # When the enter key is pressed in the textbox
    def Setuptextboxenter(self):
        print("Enter Pressed")
        print(self.TextBox.text())
        if self.Index == 0:
            Settingdic["Pathtosteam"] = self.TextBox.text()
            self.TextBox.clear()
            self.userfinder(Settingdic["Pathtosteam"])
            self.labelOne.setText("Select User")
            print("A")
        if self.Index == 1:
            Settingdic["User"] = self.TextBox.text()
            self.TextBox.clear()
        if self.Index == 2:
            Settingdic["LocalImageRepostory"] = self.TextBox.text()
            self.TextBox.clear()
        self.Index += 1
        print(Settingdic)
        return
    def userfinder(self,steamDir: str):
        LoginPath = PurePath(steamDir, "config", "loginusers.vdf")
        print(LoginPath)
        try:
            with open(LoginPath, 'r', encoding='utf-8') as f:
                data = vdf.load(f)
        except FileNotFoundError:
            print("File not found")
            erdlg = QMessageBox.critical( self,
            "Error",
            "Error: File not found please make sure you have the correct path to steam",
            buttons=QMessageBox.Ok,
            )
            self.Index -= 1
            return
        users = data.get("users", {})
        result = {}
        for steam_id, user_data in users.items():
            account_name = user_data.get("AccountName", "Unknown")
            result[steam_id] = account_name
        ASUsers = result
        print(result)
        return
    

        

# When the enter key is pressed in the textbox
# Finds to OS that is being used 
def SUOS():
    if sys.platform == "win32":
        OS = "Windows"
        Settingdic["OS"] = "Windows"
        DFPS = configL["DefaultSteamPaths"]["pathtosteamwin"]
    if sys.platform == "darwin":
        OS = "MacOS"
        Settingdic["OS"] = "MacOS"
        DFPS = str(home) + configL["DefaultSteamPaths"]["pathtosteammac"]
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
