from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from PyQt5.QtWidgets import QFileDialog

import qgis
import string


import configparser
import os


class iniFile:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.mix_config = None

    def readwrite(self, sFileName, sGroupName, sParName, sDefaultVal=""):
        self.config.read(sFileName)
        if not self.config.has_section(sGroupName):
            self.config.add_section(sGroupName)
        if not self.config.has_option(sGroupName, sParName):
            self.config.set(sGroupName, sParName, sDefaultVal)
            fp = open(sFileName, "w")
            self.config.write(fp)
        sRetVal = self.config.get(sGroupName, sParName)
        if sRetVal[0] == '"' and sRetVal[-1] == '"':
            sRetVal = sRetVal[1:-1]
        return sRetVal

    def read(self, sFileName, sGroupName, sParName, sDefaultVal=""):
        with open(sFileName, "r", encoding="cp1251") as file:
            aa = self.config.read(file)
            if not self.config.has_section(sGroupName):
                self.config.add_section(sGroupName)
            if not self.config.has_option(sGroupName, sParName):
                self.config.set(sGroupName, sParName, sDefaultVal)
            sRetVal = self.config.get(sGroupName, sParName)
            if sRetVal != "" and sRetVal[0] == '"' and sRetVal[-1] == '"':
                sRetVal = sRetVal[1:-1]
            return sRetVal

    def write(self, sFileName, sGroupName, sParName, sDefaultVal):
        self.config.read(sFileName)
        if not self.config.has_section(sGroupName):
            self.config.add_section(sGroupName)
        self.config.set(sGroupName, sParName, sDefaultVal)

        with open(sFileName, "w") as config_file:
            aa = self.config.write(config_file)

    def getIniName(self, mix_ini_name="mix_config"):
        self.mix_config = ""
        PathINI = os.getenv(mix_ini_name)
        if PathINI is None:
            PathINI = os.path.abspath(os.path.dirname(__file__) + "/mix_config.ini")
            if os.path.exists(PathINI) == True:
                self.mix_config = str(PathINI)
            else:
                self.mix_config = self.file_dialog(str(PathINI))

                if self.mix_config == "":
                    msgStr = (
                        "Не удалось считать переменную окружения MIX_CONFIG "
                        + "с указанием на ini файл\n да и файл\n"
                        + str(PathINI)
                        + "\n не найден."
                    )
                    QMessageBox.critical(
                        qgis.utils.iface.mainWindow(), "Ошибка", msgStr
                    )
        else:
            self.mix_config = str(PathINI)
        return self.mix_config

    def file_dialog(self, path="/", caption="Укажите имя INI файла", ext="*.ini"):
        return unicode(
            QFileDialog().getOpenFileName(
                qgis.utils.iface.mainWindow(), caption, path, ext
            )
        )
