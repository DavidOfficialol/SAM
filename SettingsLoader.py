from pathlib import Path
import configparser
import shutil
appVersion = "0.0.1"
configVersion = "0.1"
test = False
configL = configparser.ConfigParser()
configR = configparser.ConfigParser()
def configLoader():
    my_file = Path("config.ini")
    if my_file.is_file():
        print("config.ini found")
    else:
        print("File not found making config.ini with default")
        copy_and_rename(src="default.ini", des="config.ini", name="config.ini")
    
    configL.read("config.ini")
    
    if configL["AppSettings"]["AppVersion"] != appVersion:
        print("App Version is not the same")
        print("Updating config.ini")
        copy_and_rename(src="default.ini", des="config.ini", name="config.ini")
        configR.read("default.ini")

def configWriter():
    with open("config.ini", "w") as configfile:
        configL.write(configfile)

def copy_and_rename(src, des, name):
	# Copy the file
	shutil.copy(src, des)

if __name__ == "__main__":
    print("Running Test")
    configLoader()