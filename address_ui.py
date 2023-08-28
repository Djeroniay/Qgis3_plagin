from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)

except AttributeError:

    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(332, 275)
        DockWidget.setToolTip(_fromUtf8(""))
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtWidgets.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.leRegion = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.leRegion.setToolTip(_fromUtf8(""))
        self.leRegion.setObjectName(_fromUtf8("leRegion"))
        self.horizontalLayout_3.addWidget(self.leRegion)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.leAddress = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.leAddress.setToolTip(_fromUtf8(""))
        self.leAddress.setObjectName(_fromUtf8("leAddress"))
        self.horizontalLayout_2.addWidget(self.leAddress)
        self.pushButton_search = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_search.setObjectName(_fromUtf8("pushButton_search"))
        self.horizontalLayout_2.addWidget(self.pushButton_search)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listWidget = QtWidgets.QListWidget(self.dockWidgetContents)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_map = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_map.setObjectName(_fromUtf8("pushButton_map"))
        self.horizontalLayout.addWidget(self.pushButton_map)
        self.checkBox = QtWidgets.QCheckBox(self.dockWidgetContents)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout.addWidget(self.checkBox)
        self.pushButton_clear = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_clear.setObjectName(_fromUtf8("pushButton_clear"))
        self.horizontalLayout.addWidget(self.pushButton_clear)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)
        DockWidget.setTabOrder(self.leAddress, self.pushButton_search)
        DockWidget.setTabOrder(self.pushButton_search, self.listWidget)
        DockWidget.setTabOrder(self.listWidget, self.pushButton_clear)
        DockWidget.setTabOrder(self.pushButton_clear, self.pushButton_map)

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(
            _translate("DockWidget", "Где эта улица, где этот дом...", None)
        )
        self.label.setText(_translate("DockWidget", "Регион", None))
        self.label_2.setText(_translate("DockWidget", "Адрес ", None))
        self.pushButton_search.setText(_translate("DockWidget", "Найти", None))
        self.pushButton_map.setText(_translate("DockWidget", "Показать на карте", None))
        self.checkBox.setText(_translate("DockWidget", "последний", None))
        self.pushButton_clear.setText(_translate("DockWidget", "Очистить", None))
