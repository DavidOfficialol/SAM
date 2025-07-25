import sys
import random
import vdf
import math
from pathlib import Path, PurePath 
import glob
home = Path.home()
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QDialog, 
    QMessageBox,
    QMainWindow, 
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QScrollArea,
)
from PySide6.QtGui import QPixmap
from SteamIDStuff import *
import logging
from SettingsLoader import *
from twoby3Image import twobythreeWCImage
from datetime import datetime
Settingdic = {}
OS = ""
DFPS = ""
Setupdone = True
ASUsers = {}
game_listdic = {}
libimagelist = []
GDK = []
Now = datetime.now()
# Set up logging
logging.basicConfig(
    filename="SAM.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class MainWindow(QMainWindow):
    
    """Main window for the S.A.M"""
    def __init__(self):
        self.vt = False
        super().__init__()
        self.GLL()
        self.setWindowTitle("Steam Artwork Manger")
        self.setMinimumSize(600, 500)
        self.setBaseSize(800, 700)

        self.HBox = QHBoxLayout()
        self.Grid = QGridLayout()
        self.Scrolla = QScrollArea()
        self.MainWindow = QVBoxLayout()
        self.Wig = QWidget()

        self.HamBurMenuL = QVBoxLayout()
        self.GameListV = QPushButton("Game List")
        self.GameListV.clicked.connect(self.Test)
        self.StetinlisV = QPushButton("Settings")
        self.StetinlisV.clicked.connect(self.Test)
        self.HamBurMenuL.addWidget(self.GameListV)
        self.HamBurMenuL.addWidget(self.StetinlisV)
        self.HamBurMenuL.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.HamBurMenuL.setSpacing(10)

        self.items = []
        self.columns = 3

        for i in range(int(len(GDK))):
            Imagepath = None
            caption = None
            try:
                if Path(PurePath(Settingdic["Pathtosteam"], "appcache", "librarycache", GDK[i], "library_600x900.jpg")).is_file():
                    Imagepath = str(PurePath(Settingdic["Pathtosteam"], "appcache", "librarycache", GDK[i], "library_600x900.jpg"))
                    logging.debug(Imagepath)
                else:
                    logging.warning("Image not found: " + str(PurePath(Settingdic["Pathtosteam"], "appcache", "librarycache", GDK[i], "library_600x900.jpg")))
            except Exception as e:
                logging.error(f"Exception in main image path: {e}")
            if not Imagepath:
                try:
                    if Path(PurePath(Settingdic["Pathtosteam"], "userdata", Settingdic["accountID"][0],"config", "grid", shorten_appid(GDK[i]) + "p.png")).is_file():
                        Imagepath = str(PurePath(Settingdic["Pathtosteam"], "userdata", Settingdic["accountID"][0],"config", "grid", shorten_appid(GDK[i]) + "p.png"))
                        logging.debug("Image found in userdata: " + Imagepath) 
                    else:
                        logging.warning("Image not found in userdata: " + str(PurePath(Settingdic["Pathtosteam"], "userdata", Settingdic["accountID"][0],"config", "grid", shorten_appid(GDK[i]) + "p.png")))
                        Imagepath = ""
                except Exception as e:
                    logging.error(f"Exception in fallback image path: {e}")
                    
                    Imagepath = ""  # fallback to empty string
            # Always get caption safely
            caption = self.GLD.get(GDK[i], "Unknown") if isinstance(self.GLD, dict) else str(GDK[i])
            TTTO = twobythreeWCImage(
                imageP=Imagepath, 
                caption=caption, 
                h=150, 
                w=400, 
                Call=(lambda gameID=GDK[i], gameName=caption, imagePath=Imagepath: self.LGIV(gameID, gameName, imagePath))
            )
            TTTO.setMaximumSize(200, 450)
            self.items.append(TTTO)
        self.Grid.setSpacing(2)
        self.Wig.setLayout(self.Grid)

        self.Scrolla.setWidgetResizable(True)
        self.Scrolla.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.Scrolla.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Scrolla.setWidget(self.Wig)
        self.MainWindow.addWidget(self.Scrolla)
        self.HBox.addLayout(self.HamBurMenuL)
        self.HBox.addLayout(self.MainWindow)
        self.FWig = QWidget()
        self.FWig.setLayout(self.HBox)
        self.setCentralWidget(self.FWig)
        self.reflow_grid()
        QTimer.singleShot(0, self.reflow_grid)
        self.vt = True

    def resizeEvent(self, event):
        self.reflow_grid()
        super().resizeEvent(event)

    def reflow_grid(self):
        """Recalculate number of columns based on current width, and re-grid the items."""
        width = self.Scrolla.viewport().width()
        item_width = 210  # Account for widget width + spacing
        new_columns = max(1, width // item_width)

        if new_columns == self.columns:
            return  

        self.columns = new_columns

        # Clear current layout
        while self.Grid.count():
            item = self.Grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Re-add widgets in new layout
        for i, widget in enumerate(self.items):
            row = i // self.columns
            col = i % self.columns
            self.Grid.addWidget(widget, row, col)

        self.Grid.setSpacing(4)

    def Test(self,gameID: str, gameName: str, gameImage: str):
        print("Test")
        logging.info("Test")
        return
    def LGIV(self, gameID: str, gameName: str, gameImage: str):
            if not self.vt:
                print(str(datetime.now()) + "MainWindow not initialized")
                logging.error("MainWindow not initialized")
                return
            self.LoadGameinfoView(gameID, gameName, gameImage)

    def LoadGameinfoView(self, gameID: str, gameName: str, gameImage: str):
        print("Loading game info view for " + str(gameID))
        self.MainWindow.removeWidget(self.Scrolla)
        self.Scrolla.setParent(None)  # Properly remove from parent
        self.Scrolla.hide()           # Hide in case it's still visible
        MAINV = QVBoxLayout()
        Row1 = QHBoxLayout()

        self.GameImage = QLabel()
        self.GameImage.setPixmap(QPixmap(gameImage))
        self.GameName = QLabel(gameName)
        Row1.addWidget(self.GameName)
        Row1.addWidget(self.GameImage)
        MAINV.addLayout(Row1)
        self.MainWindow.addLayout(MAINV)



    def GLL(self):
        game_listdic = self.getlistofgames(Settingdic["Pathtosteam"], Settingdic["SteamID"], Settingdic["accountID"])
        self.libimagelistt = self.SteamImagelibary(Settingdic["Pathtosteam"])
        logging.debug(len(libimagelist))
        for key in game_listdic.keys():
            GDK.append(key)
            logging.debug(GDK)
        self.GLD = game_listdic


        logging.debug(game_listdic)
        return
    def getlistofgames(self, steamDir: str, SteamID: list, accountID: list):
        
        logging.info("Getting list of games")
        logging.debug(steamDir)
        logging.debug(str(SteamID))
        logging.debug(str(accountID))
        # Check if the steam directory exists
        library_folders_path = PurePath(steamDir ,"steamapps", "libraryfolders.vdf")
        logging.debug(library_folders_path)
        try:
            with open(library_folders_path, 'r', encoding='utf-8') as f:
                library_folders = vdf.load(f)
        except FileNotFoundError:
            logging.warning("Library folders file not found")
            return []

        game_list = {}
        for folder in library_folders.get("libraryfolders", {}).values():
            if isinstance(folder, dict):
                folder_path = folder.get("path", "")
            if folder_path:
                apps_path = PurePath(folder_path, "steamapps")
                for app_manifest in Path(apps_path).glob("appmanifest_*.acf"):
                    try:
                     with open(app_manifest, 'r', encoding='utf-8') as f:
                            app_data = vdf.load(f)
                            game_list[app_data.get("AppState", {}).get("appid", "0")] = app_data.get("AppState", {}).get("name", "Unknown")
                    except FileNotFoundError:
                        logging.error("App manifest file not found")
                        continue
        #Add non-steam games
        logging.info("steam games added")
        logging.debug(game_list)
        print(SteamID)
        for i in range(len(SteamID)):
            logging.debug(str(i))
            try:
                shortcuts_path = PurePath(steamDir, "userdata", accountID[i], "config", "shortcuts.vdf")
                with open(shortcuts_path, 'rb') as f:
                    shortcuts_data = vdf.binary_load(f)
                    for shortcut in shortcuts_data.get("shortcuts", {}).values():
                        game_list[shortcut.get("appid", "0")] = shortcut.get("appname", "Unknown")
            except FileNotFoundError:
                logging.warning("Shortcuts file not found for user " + str(accountID) + " ,this is normal if you dont have any non-steam games")
                continue
            except IndexError:
                logging.error("Index out of range for user " + str(accountID) + "")
                continue
            

        logging.info("Non-steam games added. all games added")
        logging.debug("Games found:" + str(game_list))
        return game_list
    def SteamImagelibary(self, steamDir: str):
        libImage = []
        ILCP = PurePath(steamDir, "appcache", "librarycache")
        for iLibCache in glob.glob(str(ILCP) + "/*"):
            libImage.append(iLibCache.split("/")[-1])
        logging.info("Library Cache Images recorded")
        logging.debug(libImage)
        return libImage



# Setup Windows
class setupWindows(QMainWindow):
    """Steup window for the program"""
    Index = 0
    def __init__(self):
        super().__init__()
        DPS = SUOS()
        self.setWindowTitle("S.A.M Setup")
        self.labelOne = QLabel("The Path to steam")
        self.labelOne.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTwo = QLabel("The path to your steam installaion. Please make sure you include to full path to the steam folder eg. " + DPS)
        self.labelTwo.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        logging.debug("Next Button Clicked")
        if self.Index == 3:
            logging.info("setup done")
            Settingdic["setupmode"] = "False"
            configL["AppSettings"]["setupmode"] = "False"
            configL["Steam"]["Pathtosteam"] = Settingdic["Pathtosteam"]
            for i in range(len(Settingdic["User"])):
                if i == 0:
                    configL["Steam"]["User"] = Settingdic["User"][i]
                    configL["Steam"]["SteamID"] = Settingdic["SteamID"][i]
                    configL["Steam"]["accountID"] = str(Settingdic["accountID"][i]) 
                else:
                    configL["Steam"]["User"] = configL["Steam"]["User"] + "," + Settingdic["User"][i]
                    configL["Steam"]["SteamID"] = configL["Steam"]["SteamID"] + "," + Settingdic["SteamID"][i]
                    configL["Steam"]["accountID"] = configL["Steam"]["accountID"] + "," + str(Settingdic["accountID"][i])
            configL["AppSettings"]["LocalImageRepostory"] = Settingdic["LocalImageRepostory"]
            configWriter()
            self.MW = MainWindow()
            self.MW.show() # Fixed add self. berfore MW
            self.close()
            return
        self.Setuptextboxenter()

    # When the enter key is pressed in the textbox 
    # It will check what index it is at and then set the setting to the value in the textbox and move to the next user input
    def Setuptextboxenter(self):
        logging.debug("Enter Pressed")
        logging.debug(self.TextBox.text())
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
            logging.debug("A")
        if self.Index == 1:
            Settingdic["User"] = self.TextBox.text()
            Settingdic["User"] = Settingdic["User"].split(",")
            Settingdic["SteamID"] = list(self.result.keys())
            Settingdic["accountID"] = self.accountID
            logging.debug(Settingdic["User"])
            logging.debug(Settingdic["User"])
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
        logging.info(Settingdic)
        return
    
    # When the add button is clicked it will add the current selected user to the textbox
    def addbutton(self):
        logging.debug("Add Button Clicked")
        if self.TextBox.text() == "": # If the textbox is empty it will just add the current selected user
            self.TextBox.setText(self.Commbox.currentText())
            return
        self.TextBox.setText(self.TextBox.text() + "," + self.Commbox.currentText()) # Else if the textbox is not empty it will add a comma and then the current selected user
        return

    # Load the loginusers.vdf file and get the users
    def userfinder(self,steamDir: str):
        LoginPath = PurePath(steamDir, "config", "loginusers.vdf")
        logging.debug(LoginPath)
        try:
            with open(LoginPath, 'r', encoding='utf-8') as f:
                data = vdf.load(f)
        except FileNotFoundError:
            logging.warning("File not found")
            erdlg = QMessageBox.critical( self,
            "Error",
            "Error: File not found please make sure you have the correct path to steam",
            buttons=QMessageBox.Ok,
            )
            self.Index -= 1
            logging.debug(str(self.Index))
            return
        users = data.get("users", {})
        self.result = {}
        for steam_id, user_data in users.items():
            account_name = user_data.get("AccountName", "Unknown")
            self.result[steam_id] = account_name
        logging.debug(self.result)
        self.accountID = []
        for i in range(len(self.result)):
            self.accountID.append(int(list(self.result.keys())[i]) - 76561197960265728)
            logging.debug(self.accountID)
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
    logging.info("OS: " + str(OS) + " ,DFPS: " + str(DFPS))
    return DFPS

def SDLoder():
    Settingdic["DarkMode"] = configL["AppSettings"]["DarkMode"]
    Settingdic["LocalImageRepostory"] = configL["AppSettings"]["LocalImageRepostory"]
    Settingdic["Pathtosteam"] = configL["Steam"]["Pathtosteam"]
    Settingdic["User"] = configL["Steam"]["User"]
    Settingdic["User"] = Settingdic["User"].split(",")
    Settingdic["SteamID"] = configL["Steam"]["SteamID"]
    Settingdic["SteamID"] = Settingdic["SteamID"].split(",")
    Settingdic["accountID"] = configL["Steam"]["accountID"]
    Settingdic["accountID"] = Settingdic["accountID"].split(",")
    Settingdic["Test"] = configL["AppSettings"]["Test"]
    logging.info(Settingdic)
    return Settingdic


if __name__ == "__main__":
    logging.info("Starting SAM at " + str(Now))
    app = QApplication(sys.argv)

    configLoader()
    logging.info("Config loaded")
    SUOS()
    SDLoder()
    logging.info("Settings loaded")
    if Settingdic["Test"] == "True":
        logging.info("Test mode toggled")
        logging.basicConfig(
        filename="SAM.log",
        filemode="a",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
        )
        logging.debug("Test/debug mode enabled")
    logging.info("Setup mode" + str(configL["AppSettings"]["setupmode"]))
    if configL["AppSettings"]["setupmode"] == "True" or configL["AppSettings"]["setupmode"] == "":
        Setupdone = False
        SAMSUPW = setupWindows()
        SAMSUPW.show()
    else:
        SAMwindowMain = MainWindow()
        SAMwindowMain.show()
    app.exec()
# (OvO) hello