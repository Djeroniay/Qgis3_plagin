# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QAction, QDockWidget

# from qgis.gui import QgsTextAnnotationItem

# import qgis
import string
import os
import re


from urllib.request import *
from urllib.parse import quote
import tempfile
import json


# инициализируем диалог из файл аaddress_ui.py
from .address_ui import Ui_DockWidget


class client:
    def __init__(
        self,
        proxy=None,
        user_agent="Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3",
    ):
        self.redirect_handler = HTTPRedirectHandler()
        self.http_handler = HTTPHandler()
        self.opener = build_opener(self.http_handler, self.redirect_handler)
        if proxy:
            self.proxy_handler = ProxyHandler(proxy)
            self.opener.add_handler(self.proxy_handler)
        self.opener.addheaders = [("User-agent", user_agent)]
        install_opener(self.opener)

    def request(self, url, params={}, timeout=5):
        if params:
            params = urllib.urlencode(params)
            html = urlopen(url, params, timeout)
        else:
            html = urlopen(url)
        return html.read()

    def urlretrieve(self, url, filename, params={}, timeout=5):
        if debug != 0:
            f = open(r"c:/tmp/WMS.txt", "at")
            f.write("%s\r\n" % url)
            f.close()
            pass
        req = self.request(url, params, timeout)
        f = open(filename, "wb", encoding="cp1251")
        f.write(req)
        f.close()
        return


class MixAddress:
    """поиск места по адресу"""

    def __init__(self, iface, mixOracle, config):
        self.config = config
        self.iface = iface
        self.address_crs = QgsCoordinateReferenceSystem()
        self.mix_urllib = client()

        # создание dockWidget-a
        self.dockWidgetAddress = QDockWidget("ADDRESS")  # create a new dckwidget
        self.dockWidgetAddress.ui = Ui_DockWidget()  # load the Ui script
        self.dockWidgetAddress.ui.setupUi(self.dockWidgetAddress)  # setup the ui
        self.iface.mainWindow().addDockWidget(
            Qt.LeftDockWidgetArea, self.dockWidgetAddress
        )  # add the widget to the main window

        # связывает событие нажатия на кнопку поиска адресов с методом
        self.dockWidgetAddress.ui.pushButton_search.clicked.connect(
            self.searchAddressList
        )

        # связывает событие нажатия на кнопку показа на карте с методом
        self.dockWidgetAddress.ui.pushButton_map.clicked.connect(self.searchAddressMap)

        # связывает событие двойного нажатия на строку с адресом с методом
        self.dockWidgetAddress.ui.listWidget.itemDoubleClicked.connect(
            self.searchAddressMap
        )

        # связывает событие нажатия на кнопку очистки карты с методом
        self.dockWidgetAddress.ui.pushButton_clear.clicked.connect(self.clearAddressMap)

        # установка значений по умолчанию
        self.dockWidgetAddress.ui.leRegion.setText("")
        self.dockWidgetAddress.ui.leAddress.setText("")
        self.dockWidgetAddress.setFixedHeight(268)
        self.showHideAddress()
        self.dockWidgetAddress.setVisible(True)

        # текстовые аннотации
        self.textItem = []

    def searchAddressList(self):
        """Построение списка адресов по имени улицы и номеру дома"""
        sRegion = unicode(self.dockWidgetAddress.ui.leRegion.text())
        sAddress = unicode(self.dockWidgetAddress.ui.leAddress.text())

        listWidget = self.dockWidgetAddress.ui.listWidget
        listWidget.clear()

        paramSearch = (sRegion + " " + sAddress).strip(" ")

        paramSearch = paramSearch.encode("utf-8")

        paramSearch = quote(paramSearch)

        url = self.address_url + paramSearch

        result = self.mix_urllib.request(url)

        result = unicode(result, "utf-8")

        try:
            d = json.loads(result)
        except:
            result = result[result.find("{") : -1]
            d = json.loads(result)

        try:
            d = d[int(self.address_result_tag)]
        except:
            d = d[self.address_result_tag]

        for i in range(len(d)):
            try:
                aTxt = d[i][self.address_text_tag]
                xTxt = d[i][self.address_x_tag]
                yTxt = d[i][self.address_y_tag]

                if type(xTxt) is str or type(xTxt) is unicode:
                    xTxt = re.search(self.address_x_reg_exp, xTxt).group(1)
                if type(yTxt) is str or type(yTxt) is unicode:
                    yTxt = re.search(self.address_y_reg_exp, yTxt).group(1)

                listWidget.addItem(aTxt)
                # добавляем координату точки
                listWidget.item(i).setData(32, QPointF(float(xTxt), float(yTxt)))
            except:
                listWidget.addItem("Ошибка поиска")
                pass

    def searchAddressMap(self, selItem=None):
        """Показ результата поиска по адресу на карте"""
        listWidget = self.dockWidgetAddress.ui.listWidget
        item = listWidget.currentItem()
        if item:
            myPointF = item.data(32)  # .toPointF()
            # Get the coordinates and scale factor from the dialog
            x = myPointF.x()
            y = myPointF.y()
            scale = 1
            # Get the map canvas
            mc = self.iface.mapCanvas()
            canva_crs = mc.mapSettings().destinationCrs()

            xform = QgsCoordinateTransform(
                self.address_crs, canva_crs, QgsProject.instance()
            )
            # прямое преобразование: address_crs -> canva_crs
            myPointXY = QgsPointXY(myPointF.x(), myPointF.y())
            pt1 = xform.transform(myPointXY)
            x = pt1.x()
            y = pt1.y()
            # Create a rectangle to cover the new extent
            # Увеличение в 100 раз
            extent = mc.fullExtent()

            minSize = 100
            if extent.width() > 0 and extent.height() > 0:
                minSize = min(
                    (extent.width() / 200 * scale),
                    (extent.height() / 200 * scale),
                    minSize,
                )

            xmin = float(x) - minSize
            xmax = float(x) + minSize
            ymin = float(y) - minSize
            ymax = float(y) + minSize

            rect = QgsRectangle(xmin, ymin, xmax, ymax)
            # Set the extent to our new rectangle
            mc.setExtent(rect)
            # Refresh the map
            mc.refresh()

    def clearAddressMap(self):
        """Удаление текстового элемента аннотации"""
        mc = self.iface.mapCanvas()
        # попробовать удалить существующий
        while len(self.textItem) > 0:
            try:
                mc.scene().removeItem(self.textItem[0])
            except:
                pass
            del self.textItem[0]

    def showHideAddress(self):
        """Показать/скрыть окно виджета поиска по адресу"""

        if not self.dockWidgetAddress.isVisible():
            # определение системы координат для адреса
            crsString = self.config.read(
                self.config.mix_config, "yaddress", "coordsys", "EPSG:4326"
            )
            if crsString.find("+proj") > -1:
                aa = self.address_crs.createFromProj4(crsString)
            else:
                aa = self.address_crs.createFromString(crsString)
            if not self.address_crs.isValid():
                QMessageBox.critical(
                    None,
                    "Ошибка",
                    "Не получилось определить систему координат\n%s" % crsString,
                )
                return
            self.address_url = self.config.read(
                self.config.mix_config,
                "yaddress",
                "url",
                "http://suggest-maps.yandex.ru/suggest-geo?lang=ru_RU&v=8&fullpath=1&bases=geo&add_rubrics_loc=1&add_chains_loc=1&pess_transit=1&results=20&part=",
            )
            self.address_result_tag = self.config.read(
                self.config.mix_config, "yaddress", "result_tag", "1"
            )
            self.address_text_tag = self.config.read(
                self.config.mix_config, "yaddress", "text_tag", "name"
            )
            self.address_x_tag = self.config.read(
                self.config.mix_config, "yaddress", "x_tag", "lon"
            )
            self.address_y_tag = self.config.read(
                self.config.mix_config, "yaddress", "y_tag", "lat"
            )
            self.address_x_reg_exp = self.config.read(
                self.config.mix_config, "yaddress", "x_reg_exp", "(.+)"
            )

            self.address_y_reg_exp = self.config.read(
                self.config.mix_config,
                "yaddress",
                "y_reg_exp",
                "(.+)",
            )
            self.address_region = self.config.read(
                self.config.mix_config,
                "yaddress",
                "region",
                "россия",
            )

            self.dockWidgetAddress.ui.leRegion.setText(self.address_region)

        self.dockWidgetAddress.setVisible(not self.dockWidgetAddress.isVisible())
