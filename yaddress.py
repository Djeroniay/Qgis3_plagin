# -*- coding: utf-8 -*-
"""
/***************************************************************************
 yaddress
                                 A QGIS plugin
 yaddress
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2023-08-22
        git sha              : $Format:%H$
        copyright            : (C) 2023 by PK
        email                : KolodzeevPA@kadastr.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import (
    QSettings,
    QTranslator,
    QCoreApplication,
    Qt,
    QRegExp,
    QSettings,
    QUrl,
)
from qgis.gui import QgsVertexMarker, QgsRubberBand, QgsMapToolEmitPoint

# from qgis.PyQt.QtCore import Qt, QRegExp, QSettings, QUrl
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDockWidget
from qgis.PyQt import uic

# from PyQt5.QtWidgets import QMainWindow, QDockWidget, QPushButton

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
import os.path
from .address_ui import Ui_DockWidget
from .address import MixAddress
from .mixIni import iniFile


class yaddress:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        self.config = iniFile()
        if self.config.mix_config is None:
            self.config.getIniName("mix_config_yadress")

        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "yaddress_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr("&yaddress")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("yaddress", message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
    ):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.dockWidgetAddress = None
        self.add_action(
            self.plugin_dir + "/yaddress_search.png",
            "Поиск места по ядресу",
            callback=self.searchAddress,
            # callback=self.searchAddress,
            parent=self.iface.mainWindow(),
        )
        # load the form
        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr("&yaddress"), action)
            self.iface.removeToolBarIcon(action)

    def searchAddress(self):
        """Поиск по адресу"""
        # self.mixLoad.showAddressDialog()
        if not self.dockWidgetAddress:
            self.dockWidgetAddress = MixAddress(self.iface, None, self.config)
        else:
            self.dockWidgetAddress.showHideAddress()
