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
    QComboBox,
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
        self.labelTwo.setWordWrap(True)
        LOF = self.labelOne.font()
        LOF.setPointSize(20)
        self.labelOne.setFont(LOF)
        self.TextBox = QLineEdit()
        self.TextBox.setText(DPS)
        self.but = QPushButton("Next")
        self.Commbox = QComboBox()
        self.Cbut = QPushButton("add")
        self.Commbox.hide()
        self.Cbut.hide()
        layoutt = QVBoxLayout()
        Textlayout = QHBoxLayout()
        self.Commboxlayout = QHBoxLayout()
        self.Commboxlayout.addWidget(self.Commbox)
        self.Commboxlayout.addWidget(self.Cbut)
        self.Commboxlayout.setSpacing(10)
        Textlayout.addWidget(self.TextBox)
        Textlayout.addWidget(self.but)
        Textlayout.setSpacing(10)
        layoutt.addWidget(self.labelOne)
        layoutt.addWidget(self.labelTwo)
        layoutt.addLayout(self.Commboxlayout)
        layoutt.addLayout(Textlayout)
        container = QWidget()
        container.setLayout(layoutt)
        self.setMinimumSize(500,250)
        self.setBaseSize(650,500)
        self.setCentralWidget(container)
        self.TextBox.returnPressed.connect(self.Setuptextboxenter)
        self.but.clicked.connect(self.nextbutton)
        self.Cbut.clicked.connect(self.addbutton)
    # When the next button is clicked
    def nextbutton(self):
        print("Next Button Clicked")
        if self.Index == 3:
            print("setup done")
            Settingdic["setupmode"] = "False"
            configL["AppSettings"]["setupmode"] = "False"
            configL["Steam"]["Pathtosteam"] = Settingdic["Pathtosteam"]
            for i in range(len(Settingdic["User"])):
                if i == 0:
                    configL["Steam"]["User"] = Settingdic["User"][i]
                else:
                    configL["Steam"]["User"] = configL["Steam"]["User"] + "," + Settingdic["User"][i]
            configL["AppSettings"]["LocalImageRepostory"] = Settingdic["LocalImageRepostory"]
            configWriter()
            TempMW()
            self.close()
            return
        self.Setuptextboxenter()

    # When the enter key is pressed in the textbox 
    # It will check what index it is at and then set the setting to the value in the textbox and move to the next user input
    def Setuptextboxenter(self):
        print("Enter Pressed")
        print(self.TextBox.text())
        if self.Index == 0:
            Settingdic["Pathtosteam"] = self.TextBox.text()
            self.TextBox.clear()
            self.userfinder(Settingdic["Pathtosteam"])
            if self.Index < 0: # If the userfinder function fails it will return to the previous index and will not continue on
                self.Index = 0
                return
            self.labelOne.setText("Select User")
            self.labelTwo.setText("Please select the user you want to use")
            self.Commbox.addItems(self.result.values()) 
            self.Commbox.show()
            self.Cbut.show()
            print("A")
        if self.Index == 1:
            Settingdic["User"] = self.TextBox.text()
            Settingdic["User"] = Settingdic["User"].split(",")
            print(Settingdic["User"])
            self.TextBox.clear()
            self.labelOne.setText("Local Image Repostory")
            self.labelTwo.setText("Please enter the path to the local image repostory you want to use. If you do not have one please leave this blank")
            self.Commbox.clear()
            self.Commbox.hide()
            self.Cbut.hide()
        if self.Index == 2:
            Settingdic["LocalImageRepostory"] = self.TextBox.text()
            self.TextBox.clear()
            self.labelOne.setText("Set up complete")
            self.labelTwo.setText("Setup is now complete, click ''Finish'' to continuet to the main window")
            self.TextBox.hide()
            self.but.setText("Finish")
        self.Index += 1
        print(Settingdic)
        return
    
    # When the add button is clicked it will add the current selected user to the textbox
    def addbutton(self):
        print("Add Button Clicked")
        if self.TextBox.text() == "": # If the textbox is empty it will just add the current selected user
            self.TextBox.setText(self.Commbox.currentText())
            return
        self.TextBox.setText(self.TextBox.text() + "," + self.Commbox.currentText()) # Else if the textbox is not empty it will add a comma and then the current selected user
        return

    # Load the loginusers.vdf file and get the users
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
            print(str(self.Index))
            return
        users = data.get("users", {})
        self.result = {}
        for steam_id, user_data in users.items():
            account_name = user_data.get("AccountName", "Unknown")
            self.result[steam_id] = account_name
        print(self.result)
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

def TempMW():
    MW = MainWindow()
    MW.show()
    return MW
if __name__ == "__main__":
    app = QApplication(sys.argv)

    configLoader()
    SUOS()
    SDLoder()
    print("Setup mode",configL["AppSettings"]["setupmode"])
    if configL["AppSettings"]["setupmode"] == "True" or configL["AppSettings"]["setupmode"] == "":
        Setupdone = False
        SAMSUPW = setupWindows()
        SAMSUPW.show()
    else:
        SAMwindowMain = MainWindow()
        SAMwindowMain.show()
    app.exec()
