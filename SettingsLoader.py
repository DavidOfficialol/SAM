from pathlib import Path
import configparser
import shutil
import logging

appVersion = "0.0.2"
configVersion = "0.2"
test = False
configL = configparser.ConfigParser()
configR = configparser.ConfigParser()
def configLoader():
    my_file = Path("config.ini")
    if my_file.is_file():
        print("config.ini found")
        logging.info(__name__ + " - config.ini found",)
    else:
        print("File not found making config.ini with default")
        logging.info("File not found making config.ini with default")
        copy_and_rename(src="default.ini", des="config.ini", name="config.ini")
    
    configL.read("config.ini")
    if configL["AppSettings"]["configVersion"] != configVersion:
        print("Config Version is not the same")
        logging.info("Config Version is not the same")
        print("Updating config.ini")
        logging.info("Updating config.ini")
        configR.read("default.ini")
        if configL["AppSettings"]["configVersion"] != configR["AppSettings"]["configVersion"]:
            print("Config Version is not the same")
            print("Updating config.ini")
            configL["AppSettings"]["configVersion"] = configR["AppSettings"]["configVersion"]
            configL["AppSettings"]["appVersion"] = appVersion
            for section in configR.sections():
                if section not in configL.sections():
                    configL.add_section(section)
                for key, value in configR.items(section):
                    if key not in configL[section]:
                        configL[section][key] = value
            configWriter()
    if configL["AppSettings"]["appVersion"] != appVersion:
        print("App Version is not the same")
        logging.info(__name__ + " - App Version is not the same")
        print("Updating config.ini")
        logging.info(__name__ + " - Updating config.ini")
        configL["AppSettings"]["appVersion"] = appVersion
        configWriter()
    configL.read("config.ini")
    logging.info(__name__ +" - Config Loaded")
    print("Config Loaded")


def configWriter():
    with open("config.ini", "w") as configfile:
        configL.write(configfile)

def copy_and_rename(src, des, name):
	# Copy the file
	shutil.copy(src, des)

if __name__ == "__main__":
    print("Running Test")
    configLoader()